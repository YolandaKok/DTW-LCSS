import pandas as pd
from ast import literal_eval
import gmplot
from fastdtw import fastdtw
import heapq
from haversine import haversine

def majorityVoting(idList):
    ids = []
    listLen = len(idList)

    for i in range(listLen):
        if not idList[i] in ids:
            heapq.heappush(ids, idList[i])

    #print ids
    listLen = len(ids)
    #print listLen
    if listLen == 1:
        return ids[0]
    #check for the most appearing id
    else:
        n = 0
        times = idList.count(ids[0])
        #print times

        for i in range(listLen):
            count = idList.count(ids[i])
            #print count
            if count > times:
                times = count
                n = i

        return ids[n]

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
    #push the 5 neighbors that are closer
    for i in range(2):
        distance, id = heapq.heappop(idList)
        neighbors.append(id)

    #Majority voting take the id with the most apperances in the idList
    return majorityVoting(neighbors)


#main program

#take the train set and the test set
trainSet = pd.read_csv(
    'train_set.csv', # replace with the correct path
    converters={"Trajectory": literal_eval}
)

trainSet = trainSet[0:200]

testSet = pd.read_csv(
    'train_set.csv', # replace with the correct path
    converters={"Trajectory": literal_eval}
)

testSet = testSet[0:2]

train_id = trainSet['journeyPatternId']
train_coords = trainSet['Trajectory']
test_coords = testSet['Trajectory']

id = 0
#for every journey in test set
for test in test_coords:
    print id, findNeighbors(train_coords, train_id, test)
    id += 1
