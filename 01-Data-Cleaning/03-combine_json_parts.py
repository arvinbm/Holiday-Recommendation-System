# Notes:
# This is to read the entire JSON GZ file in your computer
# Combine all the parts of extracted data from cluster since usually we have 32 json.gz zip files per 2 years extracted
# We are planning to extract GHCN Data from 1997-2022 (I'm extracting data per 2 years)
# I saved the 2-year file in a folder <year range>/ghcn in my computer
# Inside the ghcn is the 32-part json.gz file
# This program will read and combine all 32-part json.gz into 1 csv file ready for cleaning

# To run in computer: python3 03-combine_json_parts.py (make sure this script is in the same folder path as the ghcn folder that contains the 32-part json.gz file)
# Output: combined_json_parts.csv

import pandas as pd
import os
import gzip

def json_gz_to_csv(json_gz_file, csv_file):
    df = pd.read_json(json_gz_file, compression='gzip', lines=True)

    # Drop rows with blank 'state'
    # Source: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.strip.html
    df = df[df['state'].str.strip() != '']

    # Sort the DataFrame by 'state', 'year', and 'month'
    df = df.sort_values(by=['state', 'year', 'month'])

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file, index=False)

    return df

def process_json_gz_files(folder_path):
    # Initialize an empty list to store DataFrames
    dfs = []

    # Iterate through all files in the folder
    # Adapted from: https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
    for filename in os.listdir(folder_path):
        if filename.endswith(".json.gz"):
            # Create the full path to the file
            file_path = os.path.join(folder_path, filename)

            # Call the function to convert json.gz to CSV for each file
            df = json_gz_to_csv(file_path, None)

            # Append the DataFrame to the list
            dfs.append(df)

    # Concatenate all DataFrames in the list
    combined_df = pd.concat(dfs, ignore_index=True)

    return combined_df

def main():
    folder_path = 'ghcn'
    combined_data = process_json_gz_files(folder_path)

    # Display the head of the combined DataFrame
    #     display(combined_data)

    # Save the combined DataFrame to a CSV file
    output_file = 'combined_json_parts.csv'
    combined_data.to_csv(output_file, index=False)

    print(f"Combined data saved to {output_file}")

if __name__ == "__main__":
    main()
