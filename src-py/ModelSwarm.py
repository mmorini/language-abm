#ModelSwarmStep.py
import Ind
import ActionGroup
import random

import Percentile
import Stdev

class ModelSwarm:
    def __init__(self, outFile, nInds, aVal, bVal, cVal, xMin, xMax, selFreq, selVal, mutRate, debug):
        # the environment
        self.nInds = nInds
        self.indList = []

        self.debug = debug

        self.indCounter = 0

#        self.val_a =   1
#        self.val_b =  -2
#        self.val_c =  -.5
        self.val_a = aVal
        self.val_b = bVal  
        self.val_c = cVal

#        self.val_x_min = 0
#        self.val_x_max = .9
        self.val_x_min = xMin
        self.val_x_max = xMax

#        self.selectionFreq = 100    #frequenza con cui avviene la selezione sul totale dei cicli
#        self.selectionVal  =   .10 #quanti individui vengono selezionati per l'eliminazione
#        self.mutationRate  =   .01
        self.selectionFreq = selFreq    #frequenza con cui avviene la selezione sul totale dei cicli
        self.selectionVal  = selVal #quanti individui vengono selezionati per l'eliminazione
        self.mutationRate  = mutRate

        self.outFile = outFile #text dump

   # objects
    def buildObjects(self):        
        for i in range(self.nInds):
            self.indList.append(self.generateInd(i))
        
        self.indCounter = i
        
        print "GOODSTAND: Model built with ", self.indCounter + 1, " individuals"

    # actions
    def buildActions(self):

        self.indStep = ActionGroup.ActionGroup ("match")
        self.indPlay = ActionGroup.ActionGroup ("play")
        self.indAfter = ActionGroup.ActionGroup ("after")
        self.indSelection = ActionGroup.ActionGroup ("select")

        def do1(self):
            random.shuffle(self.indList)
            for aInd in self.indList:
                aInd.step()

        self.indStep.do = do1 # do is a variable linking a method

        def play(self):
            for aInd in self.indList:
                aInd.play()

        self.indPlay.do = play

        def aftermath(self):
            for aInd in self.indList:
                aInd.after()
            
        self.indAfter.do = aftermath

        def selection(self):
            cumPayoffList = []
            betaList = []
            piList = []

            for aInd in self.indList:
                cumPayoffList.append(aInd.cumPayoff)
                betaList.append(aInd.beta)
                piList.append(aInd.pi)

            cumPayoffNormList = []
            minPayoff = min(cumPayoffList)

            cumPayoffNormListZeroOne = []

            upperBoundPayoffList = []
            upperBoundVal = 0

            for n in range(len(cumPayoffList)):
                val = cumPayoffList[n] - minPayoff
                cumPayoffNormList.append(val) #normalized to positive

            sumNormPayoff = sum(cumPayoffNormList) #+ .0001 #avoid division by zero

            
            #TACUN
            #if (sumNormPayoff == 0):sumNormPayoff = 1
            if (sumNormPayoff == 0):
                if (self.debug): print "ALTERNATIVE STRATEGY"
            #alternative strategy: roulette wheel simplified
                for i in range(self.nInds): 
                    #mutation
                    if (random.uniform(0, 1) < self.mutationRate):
                        self.mutate(self.indList[i])
                        print "Mutating ind. #", self.indList[i].number
            else:        
                if (self.debug): print "STANDARD STRATEGY"
                for n in range(len(cumPayoffNormList)):
                    val = float(cumPayoffNormList[n]) / float(sumNormPayoff)
                    cumPayoffNormListZeroOne.append(val) #normalized to [0;1]
                    #print "CUMPAYOFFNORMLIST=",cumPayoffNormList[n], cumPayoffNormList
                    #print "n=", n, "cumpayoffnorm=", val, "sumNormPayoff=", sumNormPayoff
                    
                    upperBoundVal += val
                    upperBoundPayoffList.append(upperBoundVal)

            cumPayoffList.sort()

            if (self.debug): 
                print "PROVA percentile", cumPayoffList, Percentile.percentile(cumPayoffList, self.selectionVal)
                print "                ", betaList
                print "                ", piList
            
            cutoff = Percentile.percentile(cumPayoffList, self.selectionVal)

            totCumC = 0
            totCumD = 0
            totCumN = 0

            if(self.debug): refreshed = 0

            for aInd in self.indList:
            #easy strategy: below cutoff threshold, generate new random individuals
#                if (aInd.cumPayoff < cutoff): self.refreshInd(aInd)
            #alternative strategy: roulette wheel
                if (aInd.cumPayoff < cutoff): 
                    if(self.debug): refreshed += 1
                    self.cloneRWheel(aInd, upperBoundPayoffList)
                    #mutation
                    if (random.uniform(0, 1) < self.mutationRate):
                        self.mutate(aInd)
                        print "Mutating ind. #", aInd.number
                        
                totCumC += aInd.cumC
                totCumD += aInd.cumD
                totCumN += aInd.cumN

                aInd.cumPayoff = 0
                aInd.cumC = 0
                aInd.cumD = 0
                aInd.cumN = 0

            if(self.debug): print "refreshed = ", refreshed
            print "Variability in population (beta, pi): ", Stdev.stdev(betaList), Stdev.stdev(piList), "min|max (beta, pi)",\
                min(betaList), max(betaList), min(piList), max(piList)

#            print "TOTALI [C|D|N] - [beta|pi]", float(totCumC)*100/self.nInds, float(totCumD)*100/self.nInds, float(totCumN)*100/self.nInds, " - ", sum(betaList)/len(betaList), sum(piList)/len(piList)
            totCumALL = totCumC+totCumD+totCumN
            
            #TIDY OUTPUT
            outLine = "CDN|bbminp " + str( float(totCumC)/float(totCumALL) ) + ";" + str( float(totCumD)/float(totCumALL) ) + ";" + str( float(totCumN)/float(totCumALL) ) + ";" + str( sum(betaList)/len(betaList) ) + ";" + str( min(betaList)  ) + ";" + str( sum(piList)/len(piList) ) + "\n"

            print outLine
            self.outFile.write(outLine)

            #print "CDN|bp[median] ", float(totCumC)/float(totCumALL), float(totCumD)/float(totCumALL), float(totCumN)/float(totCumALL), \
                #Percentile.percentile(betaList, .5), Percentile.percentile(piList, .5)

        self.indSelection.do = selection

    
    
        self.actionGroupList = ["match", "play", "after"]
        print "-> Actions built"
        
    # actions

    def unbind(self):
        if (self.debug): print "Unbinding individuals."
        for aInd in self.indList:
            aInd.busy = 0

    def generateInd(self, i):
        beta = random.uniform(self.val_x_min, self.val_x_max)
        pi   = random.uniform(0, 1)
        return Ind.Ind(i, self, beta, pi, self.val_x_min, self.val_x_max, self.val_a, self.val_b, self.val_c)

    def refreshInd(self, aInd):
        beta = random.uniform(self.val_x_min, self.val_x_max)
        pi   = random.uniform(0, 1)
        aInd.beta = beta
        aInd.pi   = pi
        return self

    def cloneRWheel(self, aInd, ubList):
        #pick ind
        ind = -1
        wheelTurn = random.uniform(0, 1)

        #print "CRW: ubList=", ubList
        for n in range(len(ubList)):
            if wheelTurn < ubList[n]:
                ind = n
                break

        aInd.beta = self.indList[n].beta
        aInd.pi   = self.indList[n].pi
        return self

    def mutate(self, aInd):
        betaPerturbation = 0
        piPerturbation = 0

        tossA=random.uniform(0,1)
        if (tossA > .5):
            toss1=random.uniform(0,1)
            if (toss1 > .5):      
                betaPerturbation = .05
            else:
                betaPerturbation = -.05

        tossB=random.uniform(0,1)
        if (tossB > .5):
            toss2=random.uniform(0,1)
            if (toss2 > .5):      
                piPerturbation = .01
            else:
                piPerturbation = -.01

        if (self.debug): print "mutation: pre-beta, pre-pi = ", aInd.beta, aInd.pi
        aInd.beta = min(max(self.val_x_min, aInd.beta + betaPerturbation) , self.val_x_max)
        aInd.pi   = min(max(0, aInd.pi + piPerturbation) , 1)
        if (self.debug): print "mutation: post-beta, post-pi = ", aInd.beta, aInd.pi
        return self

    # step 
    def step(self, n):
        if (self.debug): 
            print "Step ", n

        self.indStep.do(self)

    #play
    def play(self, n):
        if (self.debug): 
            print "Play ", n

        self.indPlay.do(self)

    #selection
    def selection(self, n):
        if (self.debug):
            print "Selection ", n
    
        self.indSelection.do(self)
     
    #aftermath
    def aftermath(self, n):
        if (self.debug):
            print "Aftermath ", n

        self.indAfter.do(self)

    #balance
    def balance(self):
        if (self.debug):
            print "balance"

        for aInd in self.indList:
            if (self.debug): print "Individual #", aInd.number, "[pi=",aInd.pi,"] [beta=",aInd.beta,"] payoff =", aInd.cumPayoff, "[C|D|N]", aInd.cumC, aInd.cumD, aInd.cumN

    # return List of individuals
    def getIndList(self):
        return self.indList
                
    def run(self, nCycles):
        for n in range(nCycles):
            
            self.unbind()
            for s in self.actionGroupList:                
                if s == "match":
                    self.step(n)
                if s == "play":
                    self.play(n)
                if s == "after":
                    self.aftermath(n)

            if ((n != 0) and (n % self.selectionFreq == 0)):
                self.selection(n)
             
        self.balance()
            
        
        print
        print "-> Simulation completed after ", nCycles, " cycles"    
