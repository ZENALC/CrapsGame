__author__ = 'Mihir Shrestha'
from die import  Die

class CrapsGame (object):
    def __init__(self):
        self.winsCount = 0
        self.lossesCount = 0
        self.currentBet = 10
        self.startingBank = 1000
        self.currentBank = self.startingBank
        self.curentRoll = 0
        self.secondRoll = False
        self.previousRoll = 0
        self.die1 = Die(6)
        self.die2 = Die(6)
        self.payout = {4:2, 5:1.5, 6:1.2, 8:1.2, 9:1.5, 10:1.2}

    def __str__(self):
        return ("Bank: %i Wins: %i Losses: %i") % (self.getCurrentBank(), self.getWinsCount(), self.getLossesCount())
    def getCurrentRoll(self):
        return self.curentRoll
    def throw(self):
        self.curentRoll = self.die1.roll() + self.die2.roll()
        print("Roll %i" % self.curentRoll)
        if self.secondRoll == False:
            if self.curentRoll == 7 or self.curentRoll == 11:
                print("You win ")
                self.currentBank += self.currentBet
                self.winsCount += 1
            elif self. curentRoll == 2 or self.curentRoll == 3 or self.curentRoll == 12:
                self.lossesCount += 1
                self.currentBank -= self.currentBet
                print("You lost")
            else:
                self.secondRoll = True
                self.previousRoll = self.curentRoll
        else:
            if self.previousRoll == self.curentRoll:
                self.winsCount += 1
                self.currentBank += self.currentBet * self.payout[self.previousRoll]
                print("You won")
            else:
                self.lossesCount += 1
                self.currentBank -= self.currentBet * self.payout[self.previousRoll]
                print("You Lose")
                self.secondRoll = False
                
    def setCurrentBank(self, currentBank):
        self.currentBank = currentBank
    def getCurrentBank(self):
        return self.currentBank
    def setWinsCount(self, winsCount):
        self.winsCount = winsCount
    def getWinsCount(self):
        return self.winsCount
    def setLossesCount(self, lossesCount):
        self.lossesCount = lossesCount
    def getLossesCount(self):
        return self.lossesCount
    def setCurrentBet(self, currentBet):
        self.currentBet = currentBet
    def getCurrentBet(self):
        return self.currentBet
    def setStartingbank(self, startingBank):
        self.startingBank = startingBank
    def getStartingBank(self):
        return self.startingBank
    def placebet(self, betValue):
        self.setCurrentBet(betValue)
    def getCurrentRoll(self):
        return self.getCurrentRoll()