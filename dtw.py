import pandas as pd
from ast import literal_eval
import gmplot
import fastdtw
from haversine import haversine
import numpy as np
from fastdtw import fastdtw
import heapq
#from sklearn.neighbors.dist_metrics import DistanceMetric

#take the train set and teh test set
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

# Calculate the distance
for test_item in coords_final_test:
    # find the distance
    for train_item in coords_final_train:
        distance, path = fastdtw(test_item, train_item[0], dist=haversine)
        heapq.heappush(distances,(distance,train_item))
    for i in range(5):
        print heapq.heappop(distances)
    distances = []
    print "next trip"

#print trainSet.shape
#print testSet.shape

haversine = DistanceMetric.get_metric("haversine")
