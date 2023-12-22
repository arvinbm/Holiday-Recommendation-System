# CMPT-353---Group-Project

## Libraries required for the whole program
|      | Libraries |
|-----:|--------   |
|     1| pandas    |
|     2| pyspark   |
|     3| random    |
|     4| sklearn   |
|     5| numpy     |

# To run the project
  * Use the following command line: python3 holiday_location_recommendation.py 01-Data-Cleaning/weather_final.csv


## 01-Data Cleaning
- 01-ghcn_extracter.py
  * Codes Adapted from provided instructions in https://coursys.sfu.ca/2023fa-cmpt-353-d1/pages/WeatherData
  * This is to extract the GHCN weather data from SFU cluster
  * Output will be on 'ghcn-subset', you can scp them to your local or download in your computer
  * Coursys page for WeatherData contains more instructions to run this
  * ***To run in cluster:*** spark-submit 01-ghcn_extracter.py
  * ***Output:*** ghcn-subset/ghcn/<32-part_json.gz files per 2 years extracted data>

- 02-open_cluster.py
  * This is just to open one of the extracted json.gz from the previous output in the sfu cluster to check format before downloading them into your computer
  * It is important to check the format of the extracted data to ensure you have the desired columns or year (just for our peace of mind)
  * ***To run this on cluster:*** spark-submit 02-open_cluster.py <filepath/filename.json.gz>
  * ***Output:*** To view some rows of the data in cluster


- 03-combine_json_parts.py
  * Combine all the parts of extracted data from cluster since usually we have 32 json.gz zip files per 2 years extracted
  * We are planning to extract GHCN Weather Data from 1997-2022 (extracting data per 2 years since it takes 5 minutes to get this 2-year data alone)
  * Saved the 2-year file in a folder <year_range>/ghcn in personal computer to work on it
  * Inside the ghcn is the 32-part json.gz file so it looks like this example: 2015-2016/ghcn/<32-parts json.gz>
  * This program will read and combine all 32-part json.gz into 1 csv file ready for cleaning
  * Check the uploaded folder 2015-2016 to sample run this. To run, make sure to save this script inside this folder. 
  * The output 'combined_json_parts.csv' for this 2-year range is also in this folder for reference.
  * ***To run in computer:*** python3 03-combine_json_parts.py (make sure this script is in the same folder path as the ghcn folder that contains the 32-part json.gz file)
  * ***Output:*** combined_json_parts.csv 

- 04-clean_combined_json_gz.py
  * To clean, pivot and drop empty cells in order to format the combined_json_parts.csv into our desired format
  * The combined_json_parts.csv is the result of the previous step 03-combine_json_parts.py
  * Each TMAX, TMIN, PRCP, SNOW, and SNWD should be pivoted for each month
  * Check the uploaded folder 2015-2016 to sample run this. The 'combined_json_parts.csv' should be inside this folder.
  * ***To run in computer:*** python3 04-clean_combined_json_gz.py (make sure this is on the same path as combined_json_parts.csv)
  * ***Output:*** clean_output.csv
  * Check 'clean_output.csv' in the folder 2015-2016 for reference
  * Next thing we do is to rename clean_output.csv into the year range of that data file
  * Example: 2015-2016.csv
  * Save all of them into the folder 'combined_clean_data'
  * This folder should contain all cleaned data from different year range and ready to be combined into 1 csv file
  * Check the folder 'combined_clean_data' uploaded for reference

- 05-combine_all_years.py
  * To append all csv files from the folder 'combined_clean_data' since we extracted data every 2 years
  * ***To run in computer:*** python3 05-combine_all_years.py (make sure this program is in the same path as the folder 'combined_clean_data')
  * ***Output:*** 1 csv file 'combined_data.csv'
  * Now, this csv will contain all data from 1997 to 2022 ready for final touch ups!
  * Check the uploaded 'combined_data.csv' for reference

- 06-add_ghcn-states.py
  * Finally, this step adds the ghcnd-states.txt into the 'combined_data.csv'
  * We do this to add the column state_name into the corresponding state
  * The 'ghcnd-states' is txt file from the GHCN website that contains the list of state code and corresponding state name
  * We make final touch-ups and the data is ready for next steps!
  * ***To run in computer:*** python3 06-add_ghcnd-states.py
  * ***Output:***: 'weather_final.csv'
  * Make sure this program is in the same path as the file 'combined_data.csv' and 'ghcnd-states.txt'
  * Check the uploaded final output 'weather_final.csv' as well as the 'combined_data.csv' and 'ghcnd-states.txt' for reference

## 02-create_train_models.py
  * Disregard this as we moved all functions to holiday_location_recommendation.py

## 03-distance_feature.py
  * This program is an added feature for the project that involves recommending states based on their geographical proximity to a user's location

## 04-holiday_location_recommendation.py
  * After extracting and cleaning the data from the computer cluster, data is read from 01-Data-Cleaning/weather-final.csvto make a recommendation for the user’s next holiday location.

  * To do so, there is a Command Line Interface (CLI) which prompts the user for their desired season (spring, summer, fall, winter), temperature unit (celsius, fahrenheit), high temperature range, low temperature range, precipitation in mm, snowfall in mm, and snow depth in mm, user's location longitude, user's location latitude. All of these inputs are validated, and the user is asked to input a correct value if they provide an input that does not make sense (e.g., if the provided input is a string that is not convertible for a certain feature).

  * The current user's location based on longitude and latitude is used to give the best recommendation based on the distance proximity between the user and the recommended location.
  * After gathering the inputs from the user, one of four models (spring, summer, fall, winter) is trained based on the user’s desired season. In order to predict different states/provinces, the values for the maximum temperature and the minimum temperature given to the corresponding model are randomized. These random numbers for minimum and maximum temperatures are chosen from the range which the user has specified.

  * After predicting the state_name value, the user is informed of the three recommended states/provinces based on the provided answers.

### Location feature
  * This feature allows the program to sort recommendation results from closest distance to farthest distance to the user. As parameters, the following information was passed: state1, state2, state3, and the user's latitude/longitude. Using a helper function modified from the haversine formula, the feature function will return a dataframe of states ranked by their distance from the user.

  
  
## Additional Notes:

- ghcn2014-2015 folder
  * This is just our initial reference for cleaning

- monthly-data-labelled.csv
  * This file is from exercise 8, this is our desired format for the weather_final.csv after the data extraction and cleaning

- monthly-data-unlabelled.csv
  * another file from exercise 8

- state_location.csv
  * This file is used for the distance_feature.py
  
  
