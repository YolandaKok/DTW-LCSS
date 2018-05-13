import pandas as pd
from ast import literal_eval
import gmplot
import fastdtw
from sklearn.neighbors.dist_metrics import DistanceMetric

#take the train set and teh test set
trainSet = pd.read_csv(
    'train_set.csv', # replace with the correct path
    converters={"Trajectory": literal_eval}
)

testSet = pd.read_csv(
    'test_set_a1.csv', # replace with the correct path
    converters={"Trajectory": literal_eval}
)

#print trainSet.shape
#print testSet.shape

haversine = DistanceMetric.get_metric("haversine")
