# This program is a added feature for the project

import pandas as pd
import numpy as np

# The main function should read this csv
state_locations = pd.read_csv("state_location.csv")


def haversine(lat1, lon1, lat2, lon2):
    # Used code and revised from answer: https://stackoverflow.com/a/21623206
    r = 6371000  # Radius of the earth in m
    p = np.pi / 180

    a = 0.5 - np.cos((lat2 - lat1) * p) / 2 + np.cos(lat1 * p) * np.cos(lat2 * p) * (1 - np.cos((lon2 - lon1) * p)) / 2
    return 2 * r * np.arcsin(np.sqrt(a))


def rank_by_distance(state1, state2, state3, lat, lon):
    """Takes 3 recommended states' name and the user's location and return as a dataframe sorted by distance"""
    states = pd.DataFrame({'name': [state1, state2, state3]})
    merged_df = pd.merge(states, state_locations, on='name', how='left')
    merged_df['distance from you'] = haversine(lat, lon, merged_df['latitude'], merged_df['longitude'])
    merged_df = merged_df.sort_values("distance from you")

    # Or return the states as a tuple
    # return merged_df['name'].iloc[0], merged_df['name'].iloc[1], merged_df['name'].iloc[2]
    return merged_df


# Test here

s1 = 'ALBERTA'
s2 = 'ONTARIO'
s3 = 'HAWAII'

lat = 49.278847
lon = -122.915673

data = rank_by_distance(s1, s2, s3, lat, lon)
print(data)
