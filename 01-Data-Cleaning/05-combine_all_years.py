# Notes:
# This is to combine all csv files from the folder 'combined_clean_data' since we extracted data every 2 years

# To run in computer: python3 05-combine_all_years.py
#   Make sure this program is in the same path as the folder 'combined_clean_data'
# Output: 1 csv file 'combined_data.csv'
#   Now, this csv will contain all data from 1997 to 2022 ready for final touch ups

import os
import pandas as pd

def combine_and_sort_csv_files(folder_path, output_file):
    # Get a list of all CSV files in the specified folder
    # Source: https://practicaldatascience.co.uk/data-science/how-to-list-files-and-directories-with-python
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    # Check if there are any CSV files in the folder
    if not csv_files:
        print("No CSV files found in the specified folder.")
        return

    # Initialize an empty list to store individual DataFrames
    dfs = []

    # Loop through each CSV file and append its data to the list
    # Adapted from: https://python-bloggers.com/2021/09/3-ways-to-read-multiple-csv-files-for-loop-map-list-comprehension/
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        dfs.append(df)

    # Concatenate all DataFrames in the list
    combined_data = pd.concat(dfs, ignore_index=True)

    # Sort the combined DataFrame by 'state' and 'year'
    combined_data = combined_data.sort_values(by=['state', 'year'])

    # To display the data and check the columns use this
    #     # Set the display options to show all columns without truncation
    #     pd.set_option('display.max_columns', None)

    #     # Display a preview of the combined and sorted DataFrame
    #     display(combined_data)

    # Save the combined and sorted DataFrame to a new CSV file
    combined_data.to_csv(output_file, index=False)


# Specify the folder path and output file name
folder_path = 'combined_clean_data'
output_file = 'combined_data.csv'

# Call the function to combine and sort CSV files
combine_and_sort_csv_files(folder_path, output_file)

print(f"Combined data saved to {output_file}")
