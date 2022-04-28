#E37U

import csv
from findiff import FinDiff
import numpy as np


deltaAlpha = .25 #TODO define from csv
deltaBeta = .25 #TODO define from csv


# Pull in data from CSV
# Cite: https://www.geeksforgeeks.org/working-csv-files-python/

filename = 'modelData.csv' #TODO put in real CSV

rows = [] # holds data pulled from csv in a list of lists of each row

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows.append(row)
    # NOTE: could add a check for if the change in alpha and beta matches data, would be a good thing to have


#Everett Data
branchDict = {}

for i in reversed(range(int(100 * deltaAlpha),100+int(100 * deltaAlpha),int(100 * deltaAlpha))):
    print("Branch: " + str(i/100)) 
    tempBranchDict = {}
    for j in reversed(range(0,i+int(100 * deltaBeta), int(100 * deltaBeta))):
        print(str(j/100))
        tempBranchDict[(j/100)] = j #TODO Strawman
        #tempBranchDict[(j/100)] = rows[((100-i)/(100 * deltaAlpha))][(j/(100 * deltaAlpha))] #TODO Real code for importing from file
    branchDict[(i/100)] = tempBranchDict

""" for key in branchDict:
    print(key, '->', branchDict[key][key])
    #for j in range(len(brah)) """

def everettFuncDiscrete(alpha,beta): #Everett function add up of real life points, not interpolated
    return (.5 * (branchDict[alpha][alpha] - branchDict[alpha][beta]))

#relay structures 
class relay:
    def __init__(self, alphaIn, betaIn, startMemory):
        self.alpha = alphaIn
        self.beta  = betaIn
        self.memory = 0 # 1 if high at beginning of life, 0 if low at beginning of life

    def pullVal(self,x):
        if x >= self.alpha:
            self.memory = 1
            return 1
        elif x <= self.beta:
            self.memory = 0
            return 0
        else:
            return self.memory
    def paramString(self):
        return "a: " + str(self.alpha) + " b: " + str(self.beta) + " mem: " + str(self.memory)


relaySystemDict = {}

for i in reversed(range(int(100 * deltaAlpha),100+int(100 * deltaAlpha),int(100 * deltaAlpha))):
    tempRelayDict = {}
    for j in reversed(range(0,i+int(100 * deltaBeta), int(100 * deltaBeta))):
        tempRelay = relay(i/100,j/100,0) #NOTE setting default satarting value of relay memory to 0 (aka. down)
        tempRelayDict[(j/100)] = tempRelay
    relaySystemDict[(i/100)] = tempRelayDict


""" for key in relaySystemDict:
    for kyo in relaySystemDict[key]:
        print(relaySystemDict[key][kyo].paramString()) """

def relayReturn(alpha,beta,input):
    print(relaySystemDict[alpha][beta].paramString())
    return relaySystemDict[alpha][beta].pullVal(input)



# Weight Function Computation


# Adapted from example code from package docs: https://findiff.readthedocs.io/en/latest/source/examples-basic.html
alphaList = np.linspace(0,1,int(1/deltaAlpha))
betaList  = np.linspace(0,1,int(1/deltaBeta))
A,B = np.meshgrid(alphaList,betaList, indexing='ij')
f = everettFuncDiscrete(A,B)
d2_dxdy = FinDiff((0,deltaAlpha), (1,deltaBeta))
weightArray = d2_dxdy(f)

weightDict = {}

for i in reversed(range(int(100 * deltaAlpha),100+int(100 * deltaAlpha),int(100 * deltaAlpha))):
    print("Weight: " + str(i/100)) 
    tempWeightDict = {}
    for j in reversed(range(0,i+int(100 * deltaBeta), int(100 * deltaBeta))):
        print(str(j/100))
        tempWeightDict[(j/100)] = .5 * weightArray(i/100,j/100)
    weightDict[(i/100)] = tempWeightDict


#Relay test
print(relayReturn(.3,.2,.25))
print(relayReturn(.3,.2,.5))
print(relayReturn(.3,.2,.25))
print(relayReturn(.3,.2,.1))
print(relayReturn(.3,.2,.25))