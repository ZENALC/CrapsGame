__author__ = 'Mihir Shrestha'

from random import randint

class Die(object):
    def __init__(self, numberOfSides, color = "Bone", startingValue = 1, incrementValue = 1):
        self.value = 0
        self.color = color
        self.numberOfSides = numberOfSides
        self.startingValue = startingValue
        self.incrementValue = incrementValue
    def setValue(self, newValue):
        self.value = newValue
    def setColor(self, newColor):
        self.color = newColor
    def setNumberOfSide(self, sides):
        self.numberOfSides = sides
    def setStartingValue(self, value):
        self.startingValue = value
    def setIncremenValue(self, increment):
        self.incrementValue = increment
    def getColor(self):
        return self.color
    def getNumberOfSides(self):
        return self.numberOfSides
    def getValue(self):
        return self.value
    def getStartingValue(self):
        return self.startingValue
    def getIncrementValue(self):
        return self.incrementValue
    def  __str__(self):
        return str(self.value)
    def roll(self):
            self.value = randint(self.startingValue, (self.numberOfSides - 1 ) + self.startingValue)
            return self.value