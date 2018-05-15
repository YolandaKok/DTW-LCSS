import pandas as pd
import gmplot
from ast import literal_eval
import time
from haversine import haversine
import heapq

def LCSS (train_list, test_list):
    train_len = len(train_list)
    test_len = len(test_list)

    #initialize teh matrix with 0
    Matrix = [[0 for x in range(test_len + 1)] for y in range(train_len + 1)]

    match_points = 0
    match = []

    #start making the array
    for i in range(train_len + 1):
        for j in range(test_len + 1):
            if i != 0 or j != 0:
                distance = haversine(test_list[j-1], train_list[i-1], miles=False)
                if distance <= 0.2:
                    Matrix[i][j] = Matrix[i-1][j-1] + 1
                else:
                    Matrix[i][j] = max(Matrix[i-1][j], Matrix[i][j-1])

    #find the path of the match and the matching points
    i = train_len
    j = test_len

    while (i != 0 and j!= 0):
        #go to i = 0 and j = 0
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        #go up
        elif Matrix[i-1][j] == Matrix[i][j]:
            i -= 1
        #go left
        elif Matrix[i][j-1] == Matrix[i][j]:
            j -= 1
        #look diagonal
        elif Matrix[i-1][j-1] == Matrix[i][j] - 1:
            match_points += 1
            match.append(train_list[i-1])
            i -= 1
            j -= 1
        else:
            print "Huston, we have a problem"

    #return the match_points and the match
    return (match_points, match)

#main
#take the train_set and the test_set
trainSet = pd.read_csv(
    'train_set.csv', # replace with the correct path
    converters={"Trajectory": literal_eval}
)

trainSet = trainSet[0:1000]

testSet = pd.read_csv(
    'test_set_a2.csv', # replace with the correct path
    converters={"Trajectory": literal_eval}
)

train_id = trainSet['journeyPatternId']
train_coords = trainSet['Trajectory']
test_coords = testSet['Trajectory']

train_list = []
test_list = []
id = 0
test_id = 0
match_list = []

#print len(test_coords)
#for every journey in test_set
for test_coord in test_coords:
    for i in test_coord:
        t, y, x = i
        test_list.append([x,y])

    #for every journey in train_set
    for train_coord in train_coords:
        for i in train_coord:
            t, y, x = i
            train_list.append([x,y])

        (match_points, match) = LCSS (train_list, test_list)
        #make the heap
        heapq.heappush(match_list,(match_points, match, train_id, train_list))

        id += 1
        train_list = []

    #pop the heap and find the 5 nearest neighbours
    for i in range(5):
        match_points, match, train_id, train_list = heapq.heappop(match_list)
        print "mp: " + str(match_points) + str(train_id)

    match_list = []
    test_list = []
    id = 0
    test_id += 1
    print "next trip"
