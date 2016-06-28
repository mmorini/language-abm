# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 17:22:48 2016

@author: matteo danilo juste
"""

import ValidatedInput
from datetime import datetime #, date, time

import ModelSwarm

nCycles = ValidatedInput.valInputInt("How many cycles? ")

nInds = ValidatedInput.valInputInt("How many individuals? ")
nWords = ValidatedInput.valInputInt("How many words? ")
nSyll = ValidatedInput.valInputInt("How many syllables? ")

mutRate = ValidatedInput.valInputFloat("Mutation rate equals [hint: [0.01]? ")

#output file
dt = datetime.now()
fileName = dt.strftime("%Y%m%d_%H%M%S") + "out.csv"

outFile = open(fileName, "a")
outFile.write("# " + fileName + "\n") #header
outFile.write("# Inds|Words|Syllables|mutRate \n") #header
outFile.write("# " + str(nInds) + " | " + str(nWords) + " | " + str(nSyll) + " | "+ str(mutRate) + "\n") #header

print "Dumping to file: ", fileName

modelSwarm = ModelSwarm.ModelSwarm(outFile, nInds, nWords, nSyll, mutRate)
        
# create objects
modelSwarm.buildObjects()

# create actions
modelSwarm.buildActions()

# run
modelSwarm.run(nCycles)

#finishing
#modelSwarmStep.destroy()

outFile.close()
print "OUTPUT file closed."

