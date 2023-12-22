
# def getXy(df):
#     # return the X and y, y is city and X is the rest of the columns
#     return df.iloc[:, 1:], df['city']
#
#
# spring_Xy = getXy(spring_train)
# summer_Xy = getXy(summer_train)
# fall_Xy = getXy(fall_train)
# winter_Xy = getXy(winter_train)
#
# # Fit spring first
# sp_rf_model = RandomForestClassifier(n_estimators=1000, max_depth=12, oob_score=True, random_state=123)
# sp_rf_model.fit(*spring_Xy)  # Use '*' here to unpack the tuple
#
# # Access the out-of-bag score
# oob_accuracy = sp_rf_model.oob_score_
# # We don't need a very good accuracy (so maybe don't need tuning), but need a big variance so that slightly different
# # input will give a different city
#
#
# # Fit summer
# sm_rf_model = RandomForestClassifier(n_estimators=1000, max_depth=8, oob_score=True, random_state=123)
# sm_rf_model.fit(*summer_Xy)  # Use '*' here to unpack the tuple
#
# # Access the out-of-bag score
# oob_accuracy = sm_rf_model.oob_score_
#
# # Sample input
# sampleX = [42.8, 47.12, 58.46, 115, 81, 58, 0.3, 0.4, 0, 0, 0, 0]  # Don't mind of this data, I didn't know the units
# colnames = spring_train.columns[1:]
# sampleDf = pd.DataFrame(data=[sampleX], columns=colnames)
# sp_rf_model.predict(sampleDf)
#
# What are the units here.... It doesn't looks like Vancouver
# spring_train[spring_train['city'] == 'Vancouver'].mean()
#
#
# # TODO: give randomness to user input
# def randomizeInput(userInput):
#     randomized = userInput + 1  # Randomize the temperature
#     return randomized
#
#
# # TODO: Use input to predict with given model, return 5 cities
# def predictCities(userInput, seasonModel) -> tuple:
#     city1 = seasonModel.predict(randomizedInput(userInput))
#     city2 = seasonModel.predict(randomizedInput(userInput))
#     city3 = seasonModel.predict(randomizedInput(userInput))
#     city4 = seasonModel.predict(randomizedInput(userInput))
#     city5 = seasonModel.predict(randomizedInput(userInput))
#     return city1, city2, city3, city4, city5

