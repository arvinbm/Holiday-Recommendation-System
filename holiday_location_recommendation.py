import sys
import random
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import RandomForestClassifier

# Run program with: python3 holiday_location_recommendation.py 01-Data-Cleaning/combined_data.csv

def validate_input_season(user_season_input):
    while not (user_season_input == "spring" or user_season_input == "summer"
               or user_season_input == "fall" or user_season_input == "winter"):
        print("=======================================================")
        print("Invalid season input. Please try again!")
        print("=======================================================")
        user_season_input = input("When are you planning to go on holiday?\n"
                                  "Choices: (case insensitive)\n"
                                  "1. Spring (April-June)\n"
                                  "2. Summer (July-September)\n"
                                  "3. Fall (October-December)\n"
                                  "4. Winter (January-March)\n").lower()

    return user_season_input


def validate_temperature_unit(temp_unit):
    while not (temp_unit == "celsius" or temp_unit == "fahrenheit"):
        print("=======================================================")
        print("Invalid season input. Please try again!")
        print("=======================================================")
        temp_unit = input("For the next question regarding the temperature,\n"
                          "enter a temperature unit.\n"
                          "Choices: (case insensitive)\n"
                          "1. Celsius\n"
                          "2. Fahrenheit\n").lower()

    return temp_unit


def validate_low_temp_range(low_temp_range, is_celsius):
    if is_celsius:
        while not (low_temp_range == "freezing" or low_temp_range == "cold"
                   or low_temp_range == "mild"):
            print("=======================================================")
            print("Invalid range input. Please try again!")
            print("=======================================================")
            low_temp_range = input("Which category best describes your ideal low temperature range?\n"
                                   "Choices: (case insensitive):\n"
                                   "1. Mild (10°C - 25°C)\n"
                                   "2. Cold (-5°C - 10°C)\n"
                                   "3. Freezing (-20°C - -5°C)\n").lower()

    else:
        while not (low_temp_range == "freezing" or low_temp_range == "cold"
                   or low_temp_range == "mild"):
            print("=======================================================")
            print("Invalid range input. Please try again!")
            print("=======================================================")
            low_temp_range = input("Which category best describes your ideal low temperature range?\n"
                                   "Choices: (case insensitive):\n"
                                   "1. Mild (50°F - 77°F)\n"
                                   "2. Cold (23°F - 50°F)\n"
                                   "3. Freezing (-4°F - 23°F)\n").lower()
    return low_temp_range


def validate_high_temp_range(high_temp_range, is_celsius):
    if is_celsius:
        while not (high_temp_range == "hot" or high_temp_range == "cold"
                   or high_temp_range == "mild"):
            print("=======================================================")
            print("Invalid range input. Please try again!")
            print("=======================================================")
            high_temp_range = input("Which category best describes your ideal low temperature range?\n"
                                    "Choices: (case insensitive):\n"
                                    "1. Hot (25°C - 40°C)\n"
                                    "2. Mild (10°C - 25°C)\n"
                                    "3. Cold (-5°C - 10°C)\n").lower()
        else:
            while not (high_temp_range == "hot" or high_temp_range == "cold"
                       or high_temp_range == "mild"):
                print("=======================================================")
                print("Invalid range input. Please try again!")
                print("=======================================================")
                high_temp_range = input("Which category best describes your ideal low temperature range?\n"
                                        "1. Hot (77°F - 104°F)\n"
                                        "2. Mild (50°F - 77°F)\n"
                                        "3. Cold (23°F - 50°F)\n").lower()
        return high_temp_range


def validate_precipitation(precipitation_range):
    while True:
        try:
            precipitation_int = int(precipitation_range)
            if 0 <= precipitation_int <= 100:
                return precipitation_int
            else:
                print("=======================================================")
                print("Invalid precipitation input. Please enter a value between 0 and 100.")
                print("=======================================================")

            # The case where the string provided is not convertible to an integer.
        except ValueError:
            print("=======================================================")
            print("Invalid input. Please enter a valid integer.")
            print("=======================================================")

        precipitation_range = input("Enter your desired precipitation in mm.\n"
                                    "Minimum precipitation 0mm - Maximum precipitation 100mm.\n").lower()


def validate_snowfall(user_snowfall):
    while True:
        try:
            snowfall_int = int(user_snowfall)
            if 0 <= snowfall_int <= 100:
                return snowfall_int
            else:
                print("=======================================================")
                print("Invalid snowfall input. Please enter a value between 0 and 100.")
                print("=======================================================")

        # The case where the string provided is not convertible to an integer.
        except ValueError:
            print("=======================================================")
            print("Invalid input. Please enter a valid integer.")
            print("=======================================================")

        user_snowfall = input("Enter your desired snowfall in mm.\n"
                              "Minimum snowfall 0mm - Maximum snowfall 100mm\n")


def validate_snow_depth(user_snow_depth):
    while True:
        try:
            snow_depth_int = int(user_snow_depth)
            if 0 <= snow_depth_int <= 1000:
                return snow_depth_int
            else:
                print("=======================================================")
                print("Invalid snowfall input. Please enter a value between 0 and 1000.")
                print("=======================================================")

        # The case where the string provided is not convertible to an integer.
        except ValueError:
            print("=======================================================")
            print("Invalid input. Please enter a valid integer.")
            print("=======================================================")

        user_snow_depth = input("Enter your desired snow depth in mm.\n"
                                "Minimum snow depth 0mm - Maximum snow depth 1000mm\n")


def validate_user_longitude(user_longitude):
    while True:
        try:
            user_longitude = float(user_longitude)
            if -180 <= user_longitude <= 180:
                return user_longitude
            else:
                print("=======================================================")
                print("Invalid longitude input. Please enter an integer in [-180, 180) range.")
                print("=======================================================")

        # The case where the string provided is not an integer.
        except ValueError:
            print("=======================================================")
            print("Invalid input. Please enter a valid integer.")
            print("=======================================================")

        user_longitude = input("Enter your current longitude.\n"
                               "(Vancouver's longitude is -123.1216 degrees.\n")


def validate_user_latitude(user_latitude):
    while True:
        try:
            user_latitude = float(user_latitude)
            if -90 <= user_latitude <= 90:
                return user_latitude
            else:
                print("=======================================================")
                print("Invalid latitude input. Please enter an integer in [-90, 90] range.")
                print("=======================================================")

        # The case where the string provided is not an integer.
        except ValueError:
            print("=======================================================")
            print("Invalid input. Please enter a valid integer.")
            print("=======================================================")

        user_latitude = input("Enter your current latitude.\n"
                              "(Vancouver's latitude is 49.2827 degrees.)\n")


def userCLI():
    # ===== Season Input =====
    print("=======================================================")
    print("Welcome to our holiday location recommendation machine!")
    print("=======================================================")
    print("Based on your provided answers to the questions\nbelow, we would recommend"
          " your next ideal vacation\nlocation based on Machine Learning techniques.")
    print("=======================================================")

    user_ideal_season = input("When are you planning to go on holiday?\n"
                              "Choices (case insensitive):\n"
                              "1. Spring (April-June)\n"
                              "2. Summer (July-September)\n"
                              "3. Fall (October-December)\n"
                              "4. Winter (January-March)\n").lower()

    # The only valid input here is Spring, Summer, Fall, or Winter (case-insensitive).
    user_ideal_season = validate_input_season(user_ideal_season)

    # ===== Temperature Input =====
    print("=======================================================")
    temperature_unit = input("For the next question regarding the temperature,\n"
                             "enter a temperature unit.\n"
                             "Choices: (case insensitive)\n"
                             "1. Celsius\n"
                             "2. Fahrenheit\n").lower()

    # The only valid choices here are Celsius and Fahrenheit (case insensitive).
    temperature_unit = validate_temperature_unit(temperature_unit)

    low_temp_range = None
    high_temp_range = None
    if temperature_unit == "celsius":
        is_celsuis = True
        print("=======================================================")
        low_temp_range = input("Which category best describes your ideal low temperature range?\n"
                               "Choices: (case insensitive):\n"
                               "1. Mild (10°C - 25°C)\n"
                               "2. Cold (-5°C - 10°C)\n"
                               "3. Freezing (-20°C - -5°C)\n").lower()

        # The only valid choices are Cold, Mild, or Hot (case insensitive).
        low_temp_range = validate_low_temp_range(low_temp_range, is_celsuis)

        print("=======================================================")
        high_temp_range = input("Which category best describes your ideal high temperature range?\n"
                                "Choices: (case insensitive):\n"
                                "1. Hot (25°C - 40°C)\n"
                                "2. Mild (10°C - 25°C)\n"
                                "3. Cold (-5°C - 10°C)\n").lower()

        # The only valid choices are Hot, Mild, or Cold (case insensitive).
        high_temp_range = validate_high_temp_range(high_temp_range, is_celsuis)

    elif temperature_unit == "fahrenheit":
        is_celsuis = False
        print("=======================================================")
        low_temp_range = input("Which category best describes your ideal low temperature range?\n"
                               "Choices: (case insensitive):\n"
                               "1. Mild (50°F - 77°F)\n"
                               "2. Cold (23°F - 50°F)\n"
                               "3. Freezing (-4°F - 23°F)\n").lower()

        low_temp_range = validate_low_temp_range(low_temp_range, is_celsuis)

        print("=======================================================")
        high_temp_range = input("Which category best describes your ideal high temperature range?\n"
                                "Choices: (case insensitive):\n"
                                "1. Hot (77°F - 104°F)\n"
                                "2. Mild (50°F - 77°F)\n"
                                "3. Cold (23°F - 50°F)\n").lower()

        high_temp_range = validate_high_temp_range(high_temp_range, is_celsuis)

    # ===== Precipitation =====
    print("=======================================================")
    precipitation_range = input("Enter your desired precipitation in mm.\n"
                                "Minimum precipitation 0mm - Maximum precipitation 100mm\n").lower()

    precipitation_range = validate_precipitation(precipitation_range)

    # ===== Snowfall Input =====
    print("=======================================================")
    user_snowfall = input("Enter your desired snowfall in mm.\n"
                          "Minimum snowfall 0mm - Maximum snowfall 100mm\n").lower()

    user_snowfall = validate_snowfall(user_snowfall)

    # ===== Snow Depth =====
    print("=======================================================")
    user_snow_depth = input("Enter your desired snow depth in mm.\n"
                            "Minimum snow depth 0mm - Maximum snow depth 1000mm\n").lower()

    user_snow_depth = validate_snow_depth(user_snow_depth)

    # ===== Longitude & Latitude =====
    print("=======================================================")
    user_latitude = input("Enter your current latitude.\n"
                          "(Vancouver's latitude is 49.2827 degrees.)\n").lower()

    user_latitude = validate_user_latitude(user_latitude)

    print("=======================================================")
    user_longitude = input("Enter your current longitude.\n"
                           "(Vancouver's longitude is -123.1216 degrees.)\n").lower()

    user_longitude = validate_user_longitude(user_longitude)

    return user_ideal_season, temperature_unit, low_temp_range, \
           high_temp_range, precipitation_range, user_snowfall, user_snow_depth, user_longitude, user_latitude


def extract_data():
    # monthly_data_labelled = sys.argv[1]
    monthly_data_labelled = '01-Data-Cleaning/weather_final.csv'

    monthly_labelled_df = pd.read_csv(monthly_data_labelled)

    return monthly_labelled_df


def separate_initial_dataframe(monthly_labelled_df):
    # Spring: April - May - June,
    # Summer: July - August, September,
    # Fall: October - November - December,
    # Winter: January - February - March

    spring_data = monthly_labelled_df[['state_name',
                                       'tmax-04', 'tmax-05', 'tmax-06',
                                       'tmin-04', 'tmin-05', 'tmin-06',
                                       'prcp-04', 'prcp-05', 'prcp-06',
                                       'snow-04', 'snow-05', 'snow-06',
                                       'snwd-04', 'snwd-05', 'snwd-06', ]]
    summer_data = monthly_labelled_df[['state_name',
                                       'tmax-07', 'tmax-08', 'tmax-09',
                                       'tmin-07', 'tmin-08', 'tmin-09',
                                       'prcp-07', 'prcp-08', 'prcp-09',
                                       'snow-07', 'snow-08', 'snow-09',
                                       'snwd-07', 'snwd-08', 'snwd-09', ]]
    fall_data = monthly_labelled_df[['state_name',
                                     'tmax-10', 'tmax-11', 'tmax-12',
                                     'tmin-10', 'tmin-11', 'tmin-12',
                                     'prcp-10', 'prcp-11', 'prcp-12',
                                     'snow-10', 'snow-11', 'snow-12',
                                     'snwd-10', 'snwd-11', 'snwd-12', ]]
    winter_data = monthly_labelled_df[['state_name',
                                       'tmax-01', 'tmax-02', 'tmax-03',
                                       'tmin-01', 'tmin-02', 'tmin-03',
                                       'prcp-01', 'prcp-02', 'prcp-03',
                                       'snow-01', 'snow-02', 'snow-03',
                                       'snwd-01', 'snwd-02', 'snwd-03', ]]

    return spring_data, summer_data, fall_data, winter_data


def train_model(data):
    # y will be city names and X is all other columns.
    X = data[data.columns[1:]].values
    y = data['state_name'].values

    # Creating a pipeline for preprocessing and modeling.
    model = VotingClassifier(estimators=[
        ('nb', GaussianNB()),
        ('svm', SVC(kernel='linear', C=0.3)),
        ('forest', RandomForestClassifier(n_estimators=300, max_depth=10))
    ])

    model.fit(X, y)

    return model


def randomize_freezing_temp():
    return random.randint(-20, -5)


def randomize_cold_temp():
    return random.randint(-5, 10)


def randomize_mild_temp():
    return random.randint(10, 25)


def randomize_hot_temp():
    return random.randint(25, 40)


def randomize_temp(low_temp_range, high_temp_range):
    if low_temp_range == "freezing" and high_temp_range == "cold":
        month_one_high_temp = randomize_cold_temp()
        month_two_high_temp = randomize_cold_temp()
        month_three_high_temp = randomize_cold_temp()
        month_one_low_temp = randomize_freezing_temp()
        month_two_low_temp = randomize_freezing_temp()
        month_three_low_temp = randomize_freezing_temp()

    elif low_temp_range == "freezing" and high_temp_range == "mild":
        month_one_high_temp = randomize_mild_temp()
        month_two_high_temp = randomize_mild_temp()
        month_three_high_temp = randomize_mild_temp()
        month_one_low_temp = randomize_freezing_temp()
        month_two_low_temp = randomize_freezing_temp()
        month_three_low_temp = randomize_freezing_temp()

    elif low_temp_range == "freezing" and high_temp_range == "hot":
        month_one_high_temp = randomize_hot_temp()
        month_two_high_temp = randomize_hot_temp()
        month_three_high_temp = randomize_hot_temp()
        month_one_low_temp = randomize_freezing_temp()
        month_two_low_temp = randomize_freezing_temp()
        month_three_low_temp = randomize_freezing_temp()

    elif low_temp_range == "cold" and high_temp_range == "cold":
        month_one_high_temp = randomize_cold_temp()
        month_two_high_temp = randomize_cold_temp()
        month_three_high_temp = randomize_cold_temp()
        month_one_low_temp = randomize_cold_temp()
        month_two_low_temp = randomize_cold_temp()
        month_three_low_temp = randomize_cold_temp()

    elif low_temp_range == "cold" and high_temp_range == "mild":
        month_one_high_temp = randomize_mild_temp()
        month_two_high_temp = randomize_mild_temp()
        month_three_high_temp = randomize_mild_temp()
        month_one_low_temp = randomize_cold_temp()
        month_two_low_temp = randomize_cold_temp()
        month_three_low_temp = randomize_cold_temp()

    elif low_temp_range == "cold" and high_temp_range == "hot":
        month_one_high_temp = randomize_hot_temp()
        month_two_high_temp = randomize_hot_temp()
        month_three_high_temp = randomize_hot_temp()
        month_one_low_temp = randomize_cold_temp()
        month_two_low_temp = randomize_cold_temp()
        month_three_low_temp = randomize_cold_temp()

    elif low_temp_range == "mild" and high_temp_range == "cold":
        month_one_high_temp = randomize_cold_temp()
        month_two_high_temp = randomize_cold_temp()
        month_three_high_temp = randomize_cold_temp()
        month_one_low_temp = randomize_mild_temp()
        month_two_low_temp = randomize_mild_temp()
        month_three_low_temp = randomize_mild_temp()

    elif low_temp_range == "mild" and high_temp_range == "mild":
        month_one_high_temp = randomize_mild_temp()
        month_two_high_temp = randomize_mild_temp()
        month_three_high_temp = randomize_mild_temp()
        month_one_low_temp = randomize_mild_temp()
        month_two_low_temp = randomize_mild_temp()
        month_three_low_temp = randomize_mild_temp()

    else:
        month_one_high_temp = randomize_hot_temp()
        month_two_high_temp = randomize_hot_temp()
        month_three_high_temp = randomize_hot_temp()
        month_one_low_temp = randomize_mild_temp()
        month_two_low_temp = randomize_mild_temp()
        month_three_low_temp = randomize_mild_temp()

    return month_one_high_temp, month_two_high_temp, month_three_high_temp, \
           month_one_low_temp, month_two_low_temp, month_three_low_temp


def recommend_cities(low_temp_range, high_temp_range, precip_range, user_snowfall, user_snow_depth, spring_model):
    results = []

    for i in range(3):
        month_one_high_temp, month_two_high_temp, month_three_high_temp, \
        month_one_low_temp, month_two_low_temp, month_three_low_temp = randomize_temp(low_temp_range, high_temp_range)

        X = [month_one_high_temp, month_two_high_temp, month_three_high_temp, month_one_low_temp, month_two_low_temp,
             month_three_low_temp, precip_range, precip_range, precip_range, user_snowfall, user_snowfall,
             user_snowfall, user_snow_depth, user_snow_depth, user_snow_depth]

        state = spring_model.predict([X])
        results.append(state)

    return results

def haversine(lat1, lon1, lat2, lon2):
    """Returns the distance between (lat1, lon1) and (lat2, lon2)"""
    # Used code and revised from answer: https://stackoverflow.com/a/21623206
    r = 6371000  # Radius of the earth in m
    p = np.pi / 180

    a = 0.5 - np.cos((lat2 - lat1) * p) / 2 + np.cos(lat1 * p) * np.cos(lat2 * p) * (1 - np.cos((lon2 - lon1) * p)) / 2
    return 2 * r * np.arcsin(np.sqrt(a))

def rank_by_distance(state1, state2, state3, lat, lon):
    """Takes 3 recommended states' name and the user's location and return as a dataframe sorted by distance"""
    state_locations = pd.read_csv("state_location.csv")
    states = pd.DataFrame({'name': [state1, state2, state3]})
    merged_df = pd.merge(states, state_locations, on='name', how='left')
    merged_df['distance from you'] = haversine(lat, lon, merged_df['latitude'], merged_df['longitude'])
    merged_df = merged_df.sort_values("distance from you")
    merged_df = merged_df.loc[:, ['name', 'code', 'capital']].reset_index(drop=True)
    return merged_df

def main():
    # Creating the CLI to acquire user inputs.
    user_ideal_season, temperature_unit, low_temp_range, \
    high_temp_range, precipitation_range, user_snowfall, user_snow_depth, user_longitude, user_latitude = userCLI()

    # Extracting the data from the input file.
    monthly_labelled_df = extract_data()

    # Separating the initial dataframe into 4 smaller dataframes for spring, summer, fall, winter
    spring_data, summer_data, fall_data, winter_data = separate_initial_dataframe(monthly_labelled_df)

    print("=======================================================")
    print("Please be patient. Data being trained based on your answers...")
    print("=======================================================")

    # Train the models, and recommend three states/provinces based on the user inputs.
    if user_ideal_season == "spring":
        spring_model = train_model(spring_data)
        results = recommend_cities(low_temp_range, high_temp_range, precipitation_range,
                                   user_snowfall, user_snow_depth, spring_model)

    elif user_ideal_season == "summer":
        summer_model = train_model(summer_data)
        results = recommend_cities(low_temp_range, high_temp_range, precipitation_range,
                                   user_snowfall, user_snow_depth, summer_model)

    elif user_ideal_season == "fall":
        fall_model = train_model(fall_data)
        results = recommend_cities(low_temp_range, high_temp_range, precipitation_range,
                                   user_snowfall, user_snow_depth, fall_model)

    else:
        winter_model = train_model(winter_data)
        results = recommend_cities(low_temp_range, high_temp_range, precipitation_range,
                                   user_snowfall, user_snow_depth, winter_model)
    # Result ready here, rank them by distance (location feature)
    ranked_locations = rank_by_distance(results[0][0], results[1][0], results[2][0], user_latitude, user_longitude)

    print("Based on your inputs we recommend the following states or provinces for your next vacation. "
          "They are sorted by the distance from you!")
    print(ranked_locations)
    print("=======================================================")
    print("Enjoy the trip! Thanks for choosing us!")
    # print(f"1. {results[0]}\n"
    #       f"2. {results[1]}\n"
    #       f"3. {results[2]}\n")


if __name__ == "__main__":
    main()
