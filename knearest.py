import pandas as pd
import gmplot
import heapq
from ast import literal_eval
from fastdtw import fastdtw
from haversine import haversine
import sklearn
from sklearn.model_selection import KFold

def majorityVoting(idList):
    return "nothing"


# Find the K nearest neighbors
def findNeighbors(trainData, trainId, testData):
    test_list = []
    for test in testData:
        x, y, z = test
        test_list.append([z,y])

    train_list = []
    idList = []
    id = 0
    # Calculate the nearest neighbors of the training Data
    for train in trainData:
        for i in train:
            x, y, z = i
            train_list.append([z,y])
        distance = fastdtw(train_list, test_list, dist=haversine)
        #push the trainId in the heap
        heapq.heappush(idList,(distance, trainId[id]))

        train_lat = []
        train_lon = []
        id += 1

    neighbors = []
    #get the 5 neighbors that are closer
    for i in range(5):
        neighbors.append(heapq.heappop(idList))

    #Majority voting take the id with the most apperances in the idList
    return majorityVoting(neighbors)


#main program
#take the train set
trainSet = pd.read_csv(
    'train_set.csv', # replace with the correct path
    converters={"Trajectory": literal_eval}
)

trainSet = trainSet[0:100]

train_set_coords = trainSet['Trajectory']
train_set_categories = trainSet['journeyPatternId']

kf = KFold(n_splits=10)
for train_indexes, test_indexes in kf.split(trainSet):

    features_train = [train_set_coords[i] for i in train_indexes]
    features_test = [train_set_coords[i] for i in test_indexes]
    categories_train = [train_set_categories[i] for i in train_indexes]
    categories_test = [train_set_categories[i] for i in test_indexes]

    for test in features_test:
        print findNeighbors(features_train, categories_train, test)
