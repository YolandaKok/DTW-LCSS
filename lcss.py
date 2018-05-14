import pandas as pd
import gmplot
from ast import literal_eval
import time
from haversine import haversine
import heapq

#take the train_set and the test_set
trainSet = pd.read_csv(
    'train_set.csv', # replace with the correct path
    converters={"Trajectory": literal_eval}
)

trainSet = trainSet[0:10]

testSet = pd.read_csv(
    'test_set_a2.csv', # replace with the correct path
    converters={"Trajectory": literal_eval}
)

train_id = trainSet['journeyPatternId']
train_coords = trainSet['Trajectory']

test_coords = trainSet['Trajectory']

#get the distance
dist = DistanceMetric.get_metric('haversine')

train_list_lat = []
train_list_lon = []
train_list = []
test_list_lat = []
test_list_lon = []
test_list = []
lon = []
lat = []
match_points = 0
match_lat = []
match_lon = []
match = []
k = 0
h = 0

#for every journey in test_set
for test_coord in test_coords:
    for i in test_coord:
        t, y, x = i
        lat.append(x)
        lon.append(y)
    test_list_lat.append(lat)
    test_list_lon.append(lon)
    test_list.append([x,y])
    lat = []
    lon = []

    #for every journey in train_set
    for train_coord in train_coords:
        for i in train_coord:
            t, y, x = i
            lat.append(x)
            lon.append(y)
        train_list_lat.append(lat)
        train_list_lon.append(lon)
        train_list.append([x,y])
        lat = []
        lon = []
        if len(test_list) >= len(train_list):
            for i in test_list:
                point_distance = haversine(test_list[i], train_list[i], miles=False)
                if point_distance =< 200:
                    match_points += 1
                    x, y = train_list[i]
                    match_lat.append(x)
                    match_lon.append(y)
                    heapq.heappush(match,(match_points, match_lon, match_lat, train_list_lon, train_list_lat, train_id[h]))
        else:
            for i in train_list:
                point_distance = haversine(test_list[i], train_list[i], miles=False)
                if point_distance =< 200:
                    match_points += 1
                    x, y = train_list[i]
                    match_lat.append(x)
                    match_lon.append(y)
                    heapq.heappush(match,(match_points, match_lon, match_lat, train_list_lon, train_list_lat, train_id[h]))
        h += 1
        train_list_lat = []
        train_list_lon = []
        train_list = []
        match_points = []
        match_lon = []
        match_lat = []

    #take the first 5 with the best match points
    result = None
    while result is None:
        try:
            gmap = gmplot.GoogleMapPlotter.from_geocode("Dublin")
            #green part for the journey
            gmap.plot(test_list_lat, test_list_lon, color='#008000', edge_width=3)
            name = "Test" + str(k) + ".html"
            gmap.draw(name)
            result = 1
        except IndexError:
            pass
    for i in range(5):
        match_points, match_lon, match_lat, train_list_lon, train_list_lat, train_id = heapq.heappop(distances)
        result = None
        while result is None:
            try:
                gmap = gmplot.GoogleMapPlotter.from_geocode("Dublin")
                #green part for the journey
                gmap.plot(train_list_lat, train_list_lon, color='#008000', edge_width=3)
                #red part for the matching points
                gmap.plot(match_lat, match_lon, color='#FF0000', edge_width=3)
                name = "n" + str(k) + str(train_id) + ".html"
                gmap.draw(name)
                result = 1
            except IndexError:
                pass
    k += 1
    test_list = []
    test_list_lat = []
    test_list_lon = []
