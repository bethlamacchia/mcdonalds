import pandas as pd
from geopy import distance, Point

# this would be user input but for now lets just define it ourselves
zip_code = "2111"
radius = 5
# m or km, can add more but limited to the geopy package distance function
units = "m"


df = pd.read_csv("mcdonalds_clean.csv")


# since there isn't a good way to get coordinates based solely on zip code in python
# just use the data we already have and take the average, should be good enough
if str(zip_code) in df['zip'].astype(str).values:
    zip_df = df.loc[df['zip'].astype(str) == str(zip_code)]
else:
    raise ValueError("Invalid zip code.")

x_avg = zip_df['X'].mean() #lon
y_avg = zip_df['Y'].mean() #lat

center = (y_avg, x_avg)

# y is latitude and x is longitude ????
df['coordinates'] = df.apply(lambda row: Point(latitude=row['Y'], longitude=row['X']), axis=1)

df['distance_km'] = df.apply(lambda row: distance.distance(center, row['coordinates']).km, axis=1)
df['distance_miles'] = df.apply(lambda row: distance.distance(center, row['coordinates']).miles, axis=1)


if units == "m":
    solution = df.loc[df['distance_miles'].astype(float) <= radius]

elif units == "km":
    solution = df.loc[df['distance_km'].astype(float) <= radius]
else:
    print("Units provided not valid, should be m or km")

print("There are " + str(len(solution)) + " MacDonalds within " + str(radius) + units+ " of the specified zip code.")
