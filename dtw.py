import pandas as pd
from ast import literal_eval
import gmplot
from haversine import haversine
import numpy as np
from fastdtw import fastdtw
import heapq
import time

#take the train set and the test set
trainSet = pd.read_csv(
    'train_set.csv', # replace with the correct path
    converters={"Trajectory": literal_eval}
)

testSet = pd.read_csv(
    'test_set_a1.csv', # replace with the correct path
    converters={"Trajectory": literal_eval}
)

# Find the DTW distance using haversine algorithm
# Haversine calculates the distance in kilometers

# Train Data Longitude and Latitude lists
# Create a list with [lat, lon] for train_data
coords_list_train = []
coords_final_train = []
test_time = []
train_time = []
coords = trainSet['Trajectory']
train_id = trainSet['journeyPatternId']

j = 0
for item in coords:
    for i in item:
        x, y, z = i
        coords_list_train.append([z,y])
    coords_final_train.append((coords_list_train, train_id[j]))
    coords_list_train = []
    j += 1
    #x = np.array(coords_list)

# Test Data Longitude and Latitude lists
# Create a list with [lat, lon] for test_data
coords_list_test = []
coords_final_test = []
coords_test = testSet['Trajectory']

for item in coords_test:
    for i in item:
        x, y, z = i
        coords_list_test.append([z,y])
    coords_final_test.append(coords_list_test)
    coords_list_test = []

distances = []
# Ok now we have the two lists and we have to calculate the distance
# Ok
# Calculate the distance
lat = []
lon = []
k = 0
z = 0
for test_item in coords_final_test:
    # Start the clock
    start = time.time()
    # find the distance
    # Draw Test Trip
    result = None
    while result is None:
        try:
            lat, lon = zip(*test_item)
            gmap = gmplot.GoogleMapPlotter.from_geocode("Dublin")
            gmap.plot(lat, lon, color='#008000', edge_width=3)
            name = "Test Trip" + str(k) + ".html"
            gmap.draw(name)
            result = 1
        except IndexError:
            pass
    for train_item in coords_final_train:
        distance, path = fastdtw(test_item, train_item[0], dist=haversine)
        heapq.heappush(distances,(distance,train_item))
        z += 1
    for i in range(5):
        dist = heapq.heappop(distances)
        lat, lon = zip(*dist[1][0])
        result1 = None
        while result1 is None:
            try:
                gmap = gmplot.GoogleMapPlotter.from_geocode("Dublin")
                gmap.plot(lat, lon, color='#008000', edge_width=3)
                # dist[0] == idJourney
                name = dist[1][1] + "_" + str(i) + ".html"
                gmap.draw(name)

                print str(dist[0]) + " km"
                print dist[1][1] + "journeyPatternId"
                result1 = 1
            except IndexError:
                pass
    end = time.time()
    # Time elapsed
    elapsed = end - start
    print str(elapsed) + " sec"
    distances = []
    lat = []
    lon = []
    print "next trip"
    k += 1
    z = 0

#print trainSet.shape
#print testSet.shape
