#Seller.py

class Seller:
    def __init__(self, number, model, quality, price, capital, discountFactor, signalStrength):
        self.number = number
        self.model = model
        
        self.quality = quality
        self.price = price        
        self.capital = capital
        self.discountFactor = discountFactor
        
        self.lifeHorizon = 1 / (1 - discountFactor) 
        self.signal = signalStrength / self.lifeHorizon
        
        if (self.model.debug): print "Seller number ", self.number, \
     	              " has been created with quality ", self.quality, " and price ", self.price
        
    # the action
    def step(self):
        if (self.model.debug): print "Seller ", self.number , " step. My capital is", self.capital
        self.capital -= self.signal
        
    def getPrice(self):
        return self.price
    
    def getSignal(self):
        return self.signal
            
    def transact(self):
        if (self.model.debug): print "Seller ", self.number, " transacted at price ", self.getPrice()
        income = self.getPrice() - self.model.getSellerMarginalCost(self.quality)
        self.capital += income
        return self.quality