import pandas as pd
import gmplot
import heapq
from ast import literal_eval
from fastdtw import fastdtw
from haversine import haversine
import sklearn
from sklearn.model_selection import KFold

def majorityVoting(idList):
    for item in idList:
        print item[1]
    return "nothing"


# Find the K nearest neighbors
def findNeighbors(trainData, trainId, testData):
    test_list = []
    for test in testData:
        x, y, z = test
        test_list.append([z,y])

    train_list = []
    idList = []
    idi = 0
    # Calculate the nearest neighbors of the training Data
    for train in trainData:
        for i in train:
            x, y, z = i
            train_list.append([z,y])
        distance = fastdtw(train_list, test_list, dist=haversine)
        #push the trainId in the heap
        heapq.heappush(idList,(distance, trainId[idi]))

        idi += 1
        train_list = []

    neighbors = []
    # get the 5 neighbors that are closer
    for i in range(5):
        neighbors.append(heapq.heappop(idList))

    #Majority voting take the id with the most apperances in the idList
    return majorityVoting(neighbors)


# main program
# take the train set
trainSet = pd.read_csv(
    'train_set.csv', # replace with the correct path
    converters={"Trajectory": literal_eval}
)

# Read the test set
testSet = pd.read_csv(
    'test_set_a2.csv', # replace with the correct path
    converters={"Trajectory": literal_eval}
)


train_set_coords = trainSet['Trajectory']
train_set_categories = trainSet['journeyPatternId']

# Find the nearest neighbors
test_set_coords = testSet['Trajectory']

for test in test_set_coords:
    print findNeighbors(train_set_coords, train_set_categories, test)

# Ten fold cross validation
"""
kf = KFold(n_splits=10)
for train_indexes, test_indexes in kf.split(trainSet):

    features_train = [train_set_coords[i] for i in train_indexes]
    features_test = [train_set_coords[i] for i in test_indexes]
    categories_train = [train_set_categories[i] for i in train_indexes]
    categories_test = [train_set_categories[i] for i in test_indexes]
"""
