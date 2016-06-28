#ModelSwarmStep.py
import Ind
import ActionGroup
import random

import Percentile
import Stdev

class ModelSwarm:
    def __init__(self, outFile, nInds, nWords, nSyll, initVar, mutRate, debug):
        # the environment
        self.nInds = nInds
        self.nWords = nWords
        self.nSyll = nSyll
        self.indList = []

        self.debug = debug

        self.indCounter = 0

        self.initVar = initVar #initial variability of words in dictionar
        self.mutRate = mutRate #random words (syllables) muutation rate

        self.outFile = outFile #text dump

   # objects
    def buildObjects(self):
        for i in range(self.nInds):
            self.indList.append(self.generateInd(i))
        
        self.indCounter = i
        
        print "Model built with ", self.indCounter + 1, " individuals"

    # actions
    def buildActions(self):

        self.indMatch = ActionGroup.ActionGroup ("match")
        self.indComm  = ActionGroup.ActionGroup ("communicate")
        self.indInflu = ActionGroup.ActionGroup ("influence")
        self.indPlay = ActionGroup.ActionGroup ("mutate")

        #def do1(self):
        #    random.shuffle(self.indList)
        #    for aInd in self.indList:
        #        aInd.step()

        #self.indStep.do = do1 # do is a variable linking a method

        def match(self):
            for aInd in self.indList:
                aInd.play()

        self.indPlay.do = play

        def communicate(self):
            for aInd in self.indList:
                aInd.after()
            
        self.indCommunicate.do = communicate

        def influence(self):
            True            
            ###
        
        self.indInfluence.do = influence

        def mutate(self):
            True            
            ###
        self.indMutate.do = mutate
    
    
        self.actionGroupList = ["match", "communicate", "influence", "mutate"]
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
                
                
    #RUNNING ENGINE / SCHEDULER
    def run(self, nCycles):
        for n in range(nCycles):
            
            self.unbind()
            for s in self.actionGroupList:                
                if s == "match":
                    self.step(n)
                if s == "communicate":
                    self.play(n)
                if s == "influence":
                    self.aftermath(n)
                if s == "mutate":
                    self.aftermath(n)

            if ((n != 0) and (n % self.selectionFreq == 0)):
                self.selection(n)
             
        self.balance()
            
        
        print
        print "-> Simulation completed after ", nCycles, " cycles"    
