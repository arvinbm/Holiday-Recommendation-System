# Notes:
# This is to add the ghcnd_states.txt into the 'combined_data.csv'
# We do this to add the column state_name into the corresponding state
# The ghcnd_states is from the GHCN website that contains the list of state code and corresponding state name
# We make final touch-ups and the data is ready for next steps!

# To run in computer: python3 06-add_ghcnd-states.py
#   Make sure this program is in the same path as the file 'combined_data.csv'
# The final output for this Data Cleaning is 'weather_final.csv'

import pandas as pd

csv_file_path = 'combined_data.csv'
df_csv = pd.read_csv(csv_file_path)

# Read text file with state information
text_file_path = 'ghcnd-states.txt'
with open(text_file_path, 'r') as file:
    state_info_lines = file.readlines()

# Create a dictionary to map state codes to state names
state_mapping = {}
for line in state_info_lines:
    # Use slicing to take the first two elements
    # Source: https://www.w3schools.com/python/ref_string_split.asp
    state_code, state_name = line.strip().split(maxsplit=1)
    state_mapping[state_code] = state_name

# Add a new column 'state_name' to the CSV dataframe
df_csv.insert(df_csv.columns.get_loc('state') + 1, 'state_name', df_csv['state'].map(state_mapping))

# Remove rows where 'state' is equal to 'UM'
# This is necessary for the distance feature
df_csv = df_csv[df_csv['state'] != 'UM']

# Save the filtered dataframe to a new CSV file
combined_file_path = 'weather_final.csv'
df_csv.to_csv(combined_file_path, index=False)

print(f"Combined data saved to {combined_file_path}")
