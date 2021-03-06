import pandas as pd
from ast import literal_eval
import gmplot

trainSet = pd.read_csv(
    'train_set.csv', # replace with the correct path
    converters={"Trajectory": literal_eval}
)

# tripId is with the other columns
# Find 5 different journey patterns
journeys = trainSet['journeyPatternId']
journeys_trajectory = trainSet['Trajectory']
journeys_id = trainSet['tripId']

diff_journeys = []
count = -1
diff_journeys_tuple = []
diff_journeys_id = []

for journey in journeys:
    count += 1
    if journey not in diff_journeys:
        diff_journeys.append(journey)
        diff_journeys_id.append(journeys_id[count])
        if(len(diff_journeys) == 5):
            break

# Created a list
list_lat = []
list_lon = []
coords = trainSet['Trajectory']
coords = coords[0:5]
j = 0

for item in coords:
    for i in item:
        x, y, z = i
        list_lat.append(z)
        list_lon.append(y)
    result1 = None
    while result1 is None:
        try:
            gmap = gmplot.GoogleMapPlotter.from_geocode("Dublin")
            gmap.plot(list_lat, list_lon, color='#008000', edge_width=3)
            # dist[0] == idJourney
            name = str(j)
            name = "map" + name + ".html"
            gmap.draw(name)
            result1 = 1
        except IndexError:
            pass
    list_lat = []
    list_lon = []
    j += 1

print diff_journeys
print diff_journeys_id
