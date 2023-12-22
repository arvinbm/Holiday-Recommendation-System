# Notes:
# Codes Adapted from provided instructions in https://coursys.sfu.ca/2023fa-cmpt-353-d1/pages/WeatherData
# This is to extract the GHCN data from sfu cluster
# Output will be on 'ghcn-subset', you can scp them to your local or computer
# Check Coursys page for WeatherData for more instructions to run this code as per Prof Greg

# To run in cluster: spark-submit 01-ghcn_extracter.py
# Output: ghcn-subset/ghcn/<32 json.gz files per 2 years extracted data>

import sys
from pyspark.sql import SparkSession, functions, types, Row

spark = SparkSession.builder.appName('GHCN extracter').getOrCreate()

ghcn_path = '/courses/datasets/ghcn-splits'
ghcn_stations = '/courses/datasets/ghcn-more/ghcnd-stations.txt'

output = 'ghcn-subset'

observation_schema = types.StructType([
    types.StructField('station', types.StringType(), False),
    types.StructField('date', types.StringType(), False),  # becomes a types.DateType in the output
    types.StructField('observation', types.StringType(), False),
    types.StructField('value', types.IntegerType(), False),
    types.StructField('mflag', types.StringType(), False),
    types.StructField('qflag', types.StringType(), False),
    types.StructField('sflag', types.StringType(), False),
    types.StructField('obstime', types.StringType(), False),
])

station_schema = types.StructType([
    types.StructField('station', types.StringType(), False),
    types.StructField('latitude', types.FloatType(), False),
    types.StructField('longitude', types.FloatType(), False),
    types.StructField('elevation', types.FloatType(), False),
    types.StructField('state', types.StringType(), False),  # Add a field for the state
    types.StructField('name', types.StringType(), False),
])


def station_data(line):
    return [line[0:11].strip(), float(line[12:20]), float(line[21:30]), float(line[31:37]), line[38:40].strip(),
            line[41:71].strip()]


def main():
    sc = spark.sparkContext

    ## Stations data...
    stations_rdd = sc.textFile(ghcn_stations).map(station_data)
    stations = spark.createDataFrame(stations_rdd, schema=station_schema).hint('broadcast')

    ## Observations data...
    obs = spark.read.csv(ghcn_path, header=None, schema=observation_schema)

    ## Filter as we like...
    # keep only some years: still a string comparison here
    # We are trying 2014 and 2015 first
    # The GHCN data from cluster is from 1832 to 2022
    # If extracting data from cluster, it is better to do it every 2 years
    # it takes almost 5 minutes to extract 2 years of data
    obs = obs.filter((obs['date'] >= '2014') & (obs['date'] <= '2015'))

    obs = obs.filter(functions.isnull(obs['qflag']))
    obs = obs.filter(obs['observation'].isin('TMAX', 'TMIN', 'PRCP', 'SNOW', 'SNWD'))

    # parse the date string into a real date object
    obs = obs.withColumn('newdate', functions.to_date(obs['date'], 'yyyyMMdd'))

    # Extract the year from the date
    obs = obs.withColumn('year', functions.year(obs['newdate']))
    # Extract the month from the date
    obs = obs.withColumn('month', functions.month(obs['newdate']))

    # Drop unnecessary columns
    obs = obs.drop('date', 'newdate', 'mflag', 'qflag', 'sflag', 'obstime')

    # Optional, if you want the station data joined...
    obs = obs.join(stations, on='station')

    # Pivot the data to get the desired format
    pivoted_data = obs.groupBy('name', 'state', 'year', 'month').pivot('observation',
                                                                       ['TMAX', 'TMIN', 'PRCP', 'SNOW', 'SNWD'])
    pivoted_data = pivoted_data.agg(functions.first('value'))

    # Rename columns
    final_data = pivoted_data.withColumnRenamed('name', 'station_name')
    final_data = final_data.select('state', 'year', 'month', 'TMAX', 'TMIN', 'PRCP', 'SNOW', 'SNWD')

    # Drop null values
    final_data = final_data.na.drop()

    # Filter out observations without a state
    # Our Travel Recommendation Project focuses on Canada and US
    final_data = final_data.filter(final_data['state'].isNotNull())

    # Divide TMIN and TMAX values by 10 to convert into Celcius
    final_data = final_data.withColumn('TMIN', final_data['TMIN'] / 10.0)
    final_data = final_data.withColumn('TMAX', final_data['TMAX'] / 10.0)

    # Write the final data to JSON file
    final_data.write.json(output + '/ghcn', mode='overwrite', compression='gzip')

main()