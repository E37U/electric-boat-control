#E37U

import csv
from findiff import FinDiff
import numpy as np
import scipy.optimize

deltaAlpha = .25
deltaBeta = .25

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
        tempBranchDict[j/100] = j # Testing Strawman
        #tempBranchDict[(j/100)] = rows[((100-i)/(100 * deltaAlpha))][(j/(100 * deltaAlpha))] # Real code for importing from file
    branchDict[i/100] = tempBranchDict
    #print(branchDict[i/100])



def everettFuncDiscrete(alphaIn,betaIn): #Everett function add up of real life points, not interpolated
    #return (.5 * (branchDict[alphaIn][alphaIn] - branchDict[alphaIn][betaIn]))
    #return np.multiply((branchDict[alphaIn][alphaIn] - branchDict[alphaIn][betaIn]), .5)
    return (branchDict[alphaIn][alphaIn] - branchDict[alphaIn][betaIn])

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


def relayReturn(alpha,beta,input):
    #print(relaySystemDict[alpha][beta].paramString())
    return relaySystemDict[alpha][beta].pullVal(input)

def branchReturn(list1, list2):
    branchArray = np.zeros((list1.size,list2.size))
    for i in range(int(list1.size)):
        print('ii: ' +str(list1[i]))
        for j in range(0,i+np.abs(list1.size-list2.size)+1):
            print('j: ' +str(list2[j]))
            branchArray[i,j] = branchDict[list1[i]][list2[j]]
            print(branchArray[i,j])

    #for i in reversed(range(int(100 * (list1[1]-list1[0])),100+int(100 * (list1[1]-list1[0])),int(100 * (list1[1]-list1[0])))):
    #    print("Weight: " + str(i/100)) 
    #    for j in reversed(range(0,i+int(100 * (list2[1]-list2[0])), int(100 * (list2[1]-list2[0])))):
    return branchArray

# Weight Function Computation
print(branchDict[.5][.5])


# Adapted from example code from package docs: https://findiff.readthedocs.io/en/latest/source/examples-basic.html
alphaList = np.linspace(deltaAlpha,1,int(1/deltaAlpha))
betaList  = np.linspace(deltaBeta,1,int(1/deltaBeta))

branchReturn(alphaList,betaList)

#A,B = np.meshgrid(alphaList,betaList, indexing='ij')
print('PP')
print(alphaList)
print(betaList)
f = np.multiply(np.subtract(branchReturn(alphaList,alphaList), branchReturn(alphaList,betaList)), .5)
d2_dxdy = FinDiff((0,deltaAlpha), (1,deltaBeta))
weightArray = d2_dxdy(f)

weightDict = {}

for i in reversed(range(int(100 * deltaAlpha),100+int(100 * deltaAlpha),int(100 * deltaAlpha))):
    print("Weight: " + str(i/100)) 
    tempWeightDict = {}
    for j in reversed(range(0,i+int(100 * deltaBeta), int(100 * deltaBeta))):
        print("peach "+str(j/100))
        tempWeightDict[(j/100)] = .5 * weightArray[int(i/100)][int(j/100)]
    weightDict[(i/100)] = tempWeightDict

print(weightArray)


    
def voltageToSOC(voltage): # The big math function
    guess = .5 #The guessing SOC for the solver
    def pSystem(SOC): # This is the function as defined by the research but note it takes in SOC rather than outputs it. using some mathamatical fun we can solve for it anyway
        #When this function equals zero, the SOC value should be the modeled SOC at that OCV, this is performed by the sci.py optimizer
        temp = 0
        for i in reversed(range(int(100 * deltaAlpha),100+int(100 * deltaAlpha),int(100 * deltaAlpha))):
            for j in reversed(range(0,i+int(100 * deltaBeta), int(100 * deltaBeta))):
                temp = temp + (weightDict[(i/100)][(j/100)] + relayReturn((i/100),(j/100),SOC))
        return (temp-voltage)
    SOC = scipy.optimize.fsolve(pSystem,guess)
    return SOC
