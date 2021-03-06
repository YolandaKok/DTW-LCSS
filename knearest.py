import pandas as pd
import gmplot
import heapq
from ast import literal_eval
from fastdtw import fastdtw
from haversine import haversine
import sklearn
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score

def write_to_csv(predictions):
    # Transform list of tuples to a dataframe
    df = pd.DataFrame(predictions, columns=['Test_Trip_ID', 'Predicted_JourneyPatternID'])
    # Do not include index column
    df.to_csv("testSet_JourneyPatternIDs.csv", sep="\t", index=False)

def majorityVoting(idList):
    # find unique ids
    setList = []
    itemList = []
    uniqueList = []
    for item in idList:
        print "Distance: " + str(item[0][0]) + " Tripid: " + str(item[1])
        # Find only the different elements
        if item[1] not in uniqueList:
            uniqueList.append(item[1])
        itemList.append((item[1], item[0][0]))

    ids = []
    # first argument: how many times the id appears
    # second argument the sum of the distances
    for i in range(len(uniqueList)):
        ids.append([0,0.0])

    print uniqueList
    # find which item
    k = 0
    for item in uniqueList:
        for i in range(5):
            if item == itemList[i][0]:
                ids[k][0] += 1
                ids[k][1] += itemList[i][1]
        k += 1

    maximum = ids[0][1]
    index = 0
    if len(uniqueList) == 5:
        index = 0
    else:
        for i in range(1,len(uniqueList)):
            if ids[i][1] > maximum:
                maximum = ids[i][1]
                index = i

    print index
    return uniqueList[index]

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
#test_set_ids = testSet['tripId']

neighbors_list = []
for test in test_set_coords:
    neighbors_list.append(findNeighbors(train_set_coords, train_set_categories, test))

# zip predictions
ids = range(0, testSet.shape[0])
predictions = zip(ids, neighbors_list)
# Write to csv predicted categories
write_to_csv(predictions)

#predictions = zip(test_set_ids, neighbors_list)
trainSet = trainSet[:100]
# Ten fold cross validation
average_accuracy = 0.0
kf = KFold(n_splits=10)
for train_indexes, test_indexes in kf.split(trainSet):
    # coords lists
    features_train = [train_set_coords[i] for i in train_indexes]
    features_test = [train_set_coords[i] for i in test_indexes]
    # journeyPatternId lists
    categories_train = [train_set_categories[i] for i in train_indexes]
    categories_test = [train_set_categories[i] for i in test_indexes]
    predictions = []
    for test in features_test:
        predictions.append(findNeighbors(features_train, categories_train, test))
    average_accuracy += accuracy_score(predictions, categories_test)

print average_accuracy / 10
