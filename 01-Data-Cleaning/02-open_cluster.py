# Notes:
# This is to open json.gz in the sfu cluster to check format
# You can open one of the json.gz files and check format before downloading them into your computer

# To run this on cluster: spark-submit 02-open_cluster.py <filepath/name>
# Output: To view some rows of the data in cluster

from pyspark.sql import SparkSession
import sys

def process_json_file(file_path):
    # Create a Spark session
    spark = SparkSession.builder.appName("View GHCN_cluster").getOrCreate()

    # Read JSON data into a DataFrame
    df = spark.read.json(file_path)

    # Show the DataFrame
    df.show()

if __name__ == "__main__":

    # File path from the command line
    file_path = sys.argv[1]

    # Process the JSON file
    process_json_file(file_path)