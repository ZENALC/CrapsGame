__author__ = 'Mihir Shrestha'

import random

class Die(object):
    def __init__(self, numberOfSides, color = "Bone", startingValue = 1, incrementValue = 1):
        self.value = 0
        self.color = color
        self.numberOfSides = numberOfSides
        self.startingValue = startingValue
        self.incrementValue = incrementValue

    def setValue(self, newValue):
        self.value = newValue

    def getValue(self):
        return self.value

    def setColor(self, newColor):
        self.color = newColor

    def getColor(self):
        return self.color

    def setNumberOfSide(self, sides):
        self.numberOfSides = sides

    def getNumberOfSides(self):
        return self.numberOfSides

    def setStartingValue(self, value):
        self.startingValue = value

    def getStartingValue(self):
        return self.startingValue

    def setIncrementValue(self, increment):
        self.incrementValue = increment

    def getIncrementValue(self):
        return self.incrementValue

    def  __str__(self):
        return str(self.value)

    def roll(self, difficultyArg):
        if difficultyArg == 1:
            self.setValue(random.choice((7, 11)))
        elif difficultyArg == 2:
            self.setValue(random.choice((7, 11, 6, 8)))
        elif difficultyArg == 3:
            self.setValue(random.randint(self.startingValue, (self.numberOfSides - 1 ) + self.startingValue))
        elif difficultyArg == 4:
            self.setValue(random.choice((2, 3, 2, 2, 2, 2, 2, 3, 4, 5, 6, 7, 9, 10, 12)))
        else:
            self.setValue(random.choice((2, 3, 12)))

        return self.getValue()
