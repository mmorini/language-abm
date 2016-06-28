#Ind.py

import random

class Ind:
    def __init__(self, number, model, beta, pi, val_x_min, val_x_max, val_a, val_b, val_c):
        # the environment
        self.number = number
        self.model = model
        
        self.val_x_min = val_x_min
        self.val_x_max = val_x_max
        
        self.val_a = val_a
        self.val_b = val_b
        self.val_c = val_c

        self.beta = beta
        self.pi   = pi

        self.x_outcome = -999

        self.busy = 0
        self.toPlay = None
        
        self.utility = 0
        self.counterpart = None

        self.cumPayoff = 0
        self.cumC = 0
        self.cumD = 0
        self.cumN = 0

        if (self.model.debug): print "Individual number ", self.number, \
                     	        " created with beta ", beta, \
                                " and pi ", pi

    # the action
    def setFree(self):
        if (self.model.debug): print "Individual ", self.number , "set free."
        self.busy = 0

    def step(self):
        #if (self.model.debug): print "Individual ", self.number , "busy =", self.busy, " step."

        if (self.busy == 0):
            while True:
                counterpart = self.selectCounterpart(self.model.getIndList())        
                if (counterpart.busy == 0):
                    counterpart.busy = 1
                    self.busy = 1
                    self.counterpart = counterpart
                    self.counterpart.counterpart = self
                    break

            self.recap()

            
    def play(self):
        #lets play
        toss_X = random.uniform(self.val_x_min, self.val_x_max)

        if (toss_X > self.beta):
            #play C
            if (self.model.debug): print "I, #", self.number, " play C "
            self.cumC += 1
            self.toPlay = "C"
        else:
            toss_pi = random.uniform(0, 1)
            if (toss_pi < self.pi):
                #play D
                if (self.model.debug): print "I, #", self.number, " play D"
                self.cumD += 1
                self.toPlay = "D"
            else:
                if (self.model.debug): print "I, #", self.number, " play N"
                self.cumN += 1
                self.toPlay = "N"
        self.x_outcome = toss_X

        return self
        
    def recap(self):
        if (self.model.debug): print "I am #", self.number, "; my pareja is #", self.counterpart.number

    def after(self):
        if (self.model.debug): 
            print "After: payoff for", self.number, "vs", self.counterpart.number, "|", self.toPlay, self.counterpart.toPlay
        self.checkPayoff(self.toPlay, self.counterpart.toPlay)

    def checkPayoff(self, myPlay, otherPlay):
        if (myPlay == "N" or otherPlay == "N"):
            payoff = 0
        elif (myPlay == "C" and otherPlay == "C"):
            payoff = self.x_outcome
        elif (myPlay == "D" and otherPlay == "D"):
            payoff = self.val_c
        elif (myPlay == "D" and otherPlay == "C"):
            payoff = self.val_a
        elif (myPlay == "C" and otherPlay == "D"):
            payoff = self.val_b

        self.cumPayoff += payoff
        
        if (self.model.debug):
            print self.number, "gets", payoff, "totalling", self.cumPayoff

    def selectCounterpart(self, indList):
        while True:
            rndPos = random.randint(0, len(indList)-1)
            if (self.model.debug): print "ind #", rndPos, "picked"
            counterpart = indList[rndPos]
            if (counterpart.number != self.number):
                break

        return counterpart    

        
