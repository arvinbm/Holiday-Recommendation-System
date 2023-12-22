# Notes:
# This program is to clean, pivot and drop NA to format the combined_json_parts.csv into our desired format
# The combined_json_parts.csv is the result of 03-combine_json_parts.py
# Each TMAX, TMIN, PRCP, SNOW, and SNWD should be pivoted for each month

# To run in computer: python3 04-clean_combined_json_gz.py
#   make sure this is on the same path as combined_json_parts.csv
# Output: clean_output.csv

# Next thing you should do is to rename clean_output.csv into the year range of that data file
#   Example: 2015-2016.csv
# Save all of them into the folder 'combined_clean_data'
# This folder should contain all cleaned data from different year range and ready to be combined into 1 csv file
# Check the folder I uploaded for reference

import pandas as pd

def clean_csv(input_csv_file, output_csv_file):
    df = pd.read_csv(input_csv_file)

    # Drop rows with blank 'state'
    # Source: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.strip.html
    df = df[df['state'].str.strip() != '']

    # Sort the DataFrame by 'state', 'year', and 'month'
    df = df.sort_values(by=['state', 'year', 'month'])

    # Save the DataFrame to another CSV file
    df.to_csv(output_csv_file, index=False)

    return df


def main():
    input_csv_file = 'combined_json_parts.csv'
    output_csv_file = 'clean_output.csv'

    # Function to drop rows with blank 'state', and arrange by 'state', 'year', 'month'
    df = clean_csv(input_csv_file, output_csv_file)

    # Pivot the DataFrame
    df_pivoted = df.pivot_table(index=['state', 'year'], columns=['month'],
                                values=['TMAX', 'TMIN', 'PRCP', 'SNOW', 'SNWD'])

    # Flatten the multi-level columns
    # Source: https://www.geeksforgeeks.org/how-to-flatten-multiindex-in-pandas/
    df_pivoted.columns = [f'{measure.lower()}-{i:02d}' for measure in ['PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN'] for i in
                          range(1, 13)]

    # Reset the index
    df_pivoted.reset_index(inplace=True)

    df_pivoted.dropna(inplace=True)

    # To display the dataframe
    # Set the display options to show all columns without truncation
    # pd.set_option('display.max_columns', None)

    # Display the DataFrame
    #     display(df_pivoted)

    # Save the DataFrame to another CSV file
    df_pivoted.to_csv(output_csv_file, index=False)

    print(f"Combined data saved to {output_csv_file}")

if __name__ == "__main__":
    main()
