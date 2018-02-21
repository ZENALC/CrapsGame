__author__ = 'Mihir Shrestha'

from die import *
import sys
import crapsResources_rc
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5 import QtGui, uic, QtTest
from PyQt5.QtWidgets import QMainWindow, QApplication

class CrapsGame(QMainWindow):
    """A game of craps."""

    def __init__(self, parent=None):
        """Build a game with two dice."""
        self.winsCount = 0
        self.lossesCount = 0
        self.currentBet = 10
        self.startingBank = 1000
        self.currentBank = self.startingBank
        self.currentRoll = 0
        self.secondRoll = False
        self.previousRoll = 0
        self.die1 = Die(6)
        self.die2 = Die(6)
        self.die1.setValue(6)
        self.die2.setValue(6)
        self.payout = {4: 2, 5: 1.5, 6: 1.2, 8: 1.2, 9: 1.5, 10: 1.2}
        self.results ="Welcome to the game of Craps!"
        super().__init__(parent)
        uic.loadUi("crapsUI.ui", self)
        self.rollButton.clicked.connect(self.betChangedHandler)
        self.restartGame.clicked.connect(self.restart)
        self.cancelRoll.clicked.connect(self.cancelCurrentRoll)
        self.moneyBet.textChanged.connect(self.betVerifier)
        self.cancelRoll.setDisabled(True)
        self.betWins = 0
        self.betLosses = 0
        self.rollAmt = 0

    def __str__(self):
        """String representation for Dice"""
        return ""
    def getPreviousRoll(self):
        return self.previousRoll
    def setCurrentRoll(self, currentRoll):
        self.currentRoll = currentRoll
    def getCurrentRoll(self):
        return self.currentRoll
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
    def placeBet(self, betValue):
        self.setCurrentBet(betValue)

    def updateUI(self):
        if self.getCurrentBank() <= 0:
            self.hint.setText('Game over. You rolled the dice a total of %i times. Click restart to play again!' % self.rollAmt)
            self.rollButton.setEnabled(False)
            self.moneyBet.setEnabled(False)
        self.winsLabel.setText(str(self.getWinsCount()))
        self.lossesLabel.setText(str(self.getLossesCount()))
        self.resultLabel.setText(self.results)
        self.die1View.setPixmap(QtGui.QPixmap(":/" + str(self.die1.getValue())))
        self.die2View.setPixmap(QtGui.QPixmap(":/" + str(self.die2.getValue())))
        self.bank.setText(str("$" + str(self.getCurrentBank())))
        self.netProfit.setText("$" + str(self.currentBank - self.startingBank))
        self.profitAmt.setText("$ +" + str(self.betWins))
        self.lossAmt.setText("$ -" + str(self.betLosses))

    @pyqtSlot() #player asked fora roll
    def rollButtonClikedHandler(self):
        self.rollAmt += 1
        self.hint.setText("")
        self.currentRoll = self.die1.roll() + self.die2.roll()
        self.results = "You rolled a %i and will have to roll again to win money." % (self.currentRoll)
        if self.secondRoll == False:
            if self.currentRoll == 7 or self.currentRoll == 11:
                self.results = "You win $%i!" % self.getCurrentBet()
                self.betWins += self.getCurrentBet()
                self.currentBank += self.getCurrentBet()
                self.winsCount += 1
            elif self.currentRoll == 2 or self.currentRoll == 3 or self.currentRoll == 12:
                self.results = "You lose $%i!" % self.getCurrentBet()
                self.betLosses += self.getCurrentBet()
                self.lossesCount += 1
                self.currentBank -= self.getCurrentBet()
            else:
                self.secondRoll = True
                self.previousRoll = self.currentRoll
                self.hint.setText("You may also choose to not roll again to only lose your placed amount bet without payout ratios.")
                self.moneyBet.setEnabled(False)
                self.cancelRoll.setEnabled(True)
        else:
            if self.previousRoll == self.currentRoll:
                self.winsCount += 1
                self.betAmt = int(self.getCurrentBet() * self.payout[self.getPreviousRoll()])
                self.currentBank += self.betAmt
                self.results = "You win $%i!" % self.betAmt
                self.betWins += self.betAmt
            else:
                self.lossesCount += 1
                self.betAmt = int(self.getCurrentBet() * self.payout[self.getPreviousRoll()])
                self.currentBank -= self.betAmt
                self.results = "You lose $%i!" % self.betAmt
                self.betLosses += self.betAmt
            self.moneyBet.setEnabled(True)
            self.cancelRoll.setEnabled(False)
            self.secondRoll = False
        self.updateUI()

    def betVerifier(self):
        try:
            moneyBet = int(self.moneyBet.toPlainText())
            if moneyBet <= 0:
                self.results = "You cannot bet with amounts less than 0 or 0 itself."
                self.rollButton.setEnabled(False)
            elif moneyBet > self.getCurrentBank():
                self.results = "Error, you cannot bet with what you do not have. Please try again."
                self.rollButton.setEnabled(False)
            else:
                self.results = "Would you like to bet with $%i?" % moneyBet
                self.rollButton.setEnabled(True)
        except:
            moneyBet2 = self.moneyBet.toPlainText()
            if moneyBet2 == "":
                self.results = "Please type in something as a bet. You cannot bet nothing."
                self.rollButton.setEnabled(False)
            else:
                self.results = "Please type in an integer as a bet."
                self.rollButton.setEnabled(False)
        self.updateUI()

    @pyqtSlot() #player asked for a roll
    def betChangedHandler(self):
        try:
            moneyBet = int(self.moneyBet.toPlainText())
            if self.getCurrentBank() <= 0:
                self.results = "Game over. You rolled the dice a total of %i times." % self.rollAmt
                self.hint.setText('Click restart to play again!')
                self.rollButton.setEnabled(False)
                self.moneyBet.setEnabled(False)
            elif moneyBet <= 0:
                self.results = "You cannot bet with amounts less than 0 or 0 itself."
                self.rollButton.setEnabled(False)
            elif moneyBet <= self.getCurrentBank():
                self.setCurrentBet(int(self.moneyBet.toPlainText()))
                self.rollButtonClikedHandler()
            else:
                self.results = "Error, you cannot bet with what you do not have. Please try again."
                self.rollButton.setEnabled(False)
        except:
            self.results = "Please type in an integer as a bet."
            self.rollButton.setEnabled(False)
        self.updateUI()

    def cancelCurrentRoll(self):
        self.currentBank -= self.currentBet
        self.results = "You have decided to not roll and have lost your initial bet amount of $%i." % self.getCurrentBet()
        self.betLosses += self.currentBet
        self.hint.setText("")
        self.updateUI()
        self.cancelRoll.setEnabled(False)
        self.moneyBet.setEnabled(True)

    def restart(self):
        self.winsCount = 0
        self.lossesCount = 0
        self.currentBet = 10
        self.startingBank = 1000
        self.currentBank = self.startingBank
        self.currentRoll = 0
        self.secondRoll = False
        self.previousRoll = 0
        self.results = "You have restarted the game."
        self.moneyBet.setEnabled(True)
        self.hint.setText("")
        self.rollButton.setEnabled(True)
        self.cancelRoll.setEnabled(False)
        self.betWins = 0
        self.betLosses = 0
        self.rollAmt = 0
        self.updateUI()

if __name__== "__main__":
    app = QApplication(sys.argv)
    crapsApp = CrapsGame()
    crapsApp.updateUI()
    crapsApp.show()
    sys.exit(app.exec_())