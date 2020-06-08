import logging
import sys
import os
from pickle import load, dump

from PyQt5 import QtGui, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox

import craps_rc
from crapsGame.die import *


class AchievementWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join('UI Files', 'achievements.ui'), self)


class HelpWindow(QDialog):
    def __init__(self, parent=None):
        # super(HelpWindow, self).__init__(parent)
        super().__init__(parent)
        uic.loadUi(os.path.join('UI Files', 'achievements.ui'), self)
        if crapsApp.initializationLogging:
            logging.info("Initialized help app")


class AppStats(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join('UI Files', 'stats.ui'), self)


def classicThemeApply():
    if crapsApp.methodsLogging:
        logging.info("Called classicThemeApply method")

    crapsApp.centralwidget.setStyleSheet("")
    crapsApp.statusbar.setStyleSheet("")
    crapsApp.theme = "classic"


class AppSettings(QDialog):
    def __init__(self, parent=None):
        # super(AppSettings, self).__init__(parent)
        super().__init__(parent)
        uic.loadUi(os.path.join('UI Files', 'settings.ui'), self)

        if crapsApp.initializationLogging:
            logging.info("Initialized settings app")

        self.buttonBox.accepted.connect(crapsApp.saveSettings)
        self.buttonBox.rejected.connect(lambda: self.close())

        self.restartButton.clicked.connect(crapsApp.restart)
        self.clearLog.clicked.connect(crapsApp.deleteLog)
        self.restoreButton.clicked.connect(self.restoreEverything)

        self.alwaysWinButton.toggled.connect(lambda: crapsApp.changeDifficulty(1))
        self.easyButton.toggled.connect(lambda: crapsApp.changeDifficulty(2))
        self.mediumButton.toggled.connect(lambda: crapsApp.changeDifficulty(3))
        self.hardButton.toggled.connect(lambda: crapsApp.changeDifficulty(4))
        self.impossibleButton.toggled.connect(lambda: crapsApp.changeDifficulty(5))
        self.enabledCheck.toggled.connect(self.loggingControl)

        self.classicTheme.toggled.connect(classicThemeApply)
        self.rainbowTheme.toggled.connect(self.rainbowThemeApply)
        self.laNoireTheme.toggled.connect(self.laNoireThemeApply)
        self.naturalTheme.toggled.connect(self.naturalThemeApply)

        if crapsApp.theme == "classic":
            classicThemeApply()
            self.classicTheme.setChecked(True)

        elif crapsApp.theme == "rainbow":
            self.rainbowThemeApply()
            self.rainbowTheme.setChecked(True)

        elif crapsApp.theme == "laNoire":
            self.laNoireThemeApply()
            self.laNoireTheme.setChecked(True)

        elif crapsApp.theme == "natural":
            self.naturalThemeApply()
            self.naturalTheme.setChecked(True)

        self.difficultyButton = [self.alwaysWinButton, self.easyButton, self.mediumButton, self.hardButton,
                                 self.impossibleButton]
        self.difficultyButton[crapsApp.difficultyLevel - 1].setChecked(True)

        self.startingBankSpin.setValue(crapsApp.startingBank)
        self.minimumBetSpin.setValue(crapsApp.minimumBet)
        self.maximumBetSpin.setValue(crapsApp.maximumBet)

        if crapsApp.logging:
            self.enabledCheck.setChecked(True)

            if crapsApp.difficultyLogging:
                self.difficultyCheck.setChecked(True)

            if crapsApp.winsLogging:
                self.winsCheck.setChecked(True)

            if crapsApp.methodsLogging:
                self.methodsCheck.setChecked(True)

            if crapsApp.rollsLogging:
                self.rollsCheck.setChecked(True)

            if crapsApp.errorsLogging:
                self.errorsCheck.setChecked(True)

            if crapsApp.lossesLogging:
                self.lossesCheck.setChecked(True)

            if crapsApp.bankLogging:
                self.bankCheck.setChecked(True)

            if crapsApp.initializationLogging:
                self.initializationCheck.setChecked(True)

            if crapsApp.warningsLogging:
                self.warningsCheck.setChecked(True)

            self.loggingOptions = [crapsApp.difficultyLogging, crapsApp.winsLogging, crapsApp.methodsLogging,
                                   crapsApp.rollsLogging, crapsApp.errorsLogging, crapsApp.lossesLogging,
                                   crapsApp.bankLogging, crapsApp.initializationLogging, crapsApp.warningsLogging]

    def restoreEverything(self):
        crapsApp.difficultyLevel = 3
        crapsApp.minimumBet = 1
        crapsApp.maximumBet = 1000
        crapsApp.startingBank = 1000

        self.startingBankSpin.setValue(1000)
        self.minimumBetSpin.setValue(1)
        self.maximumBetSpin.setValue(1000)

        self.mediumButton.setChecked(True)
        classicThemeApply()
        self.classicTheme.setChecked(True)
        self.enabledCheck.setChecked(False)
        self.loggingControl()

    @staticmethod
    def rainbowThemeApply():
        if crapsApp.methodsLogging:
            logging.info("Called rainbowThemeApply method")

        crapsApp.centralwidget.setStyleSheet("background-color: #329992; color: black")
        crapsApp.statusbar.setStyleSheet("background-color: #329992; color: black;")
        crapsApp.theme = "rainbow"

    @staticmethod
    def laNoireThemeApply():
        if crapsApp.methodsLogging:
            logging.info("Called laNoireThemeApply method")

        crapsApp.centralwidget.setStyleSheet("background-color: #462E2E; color: white;")
        crapsApp.statusbar.setStyleSheet("background-color: #462E2E; color: white;")
        crapsApp.theme = "laNoire"

    @staticmethod
    def naturalThemeApply():
        if crapsApp.methodsLogging:
            logging.info("Called naturalThemeApply method")

        crapsApp.centralwidget.setStyleSheet("background-color: #8ff442; color: #000000;")
        crapsApp.statusbar.setStyleSheet("background-color: #8ff442; color: #000000;")
        crapsApp.theme = "natural"

    def loggingControl(self):
        if crapsApp.methodsLogging:
            logging.info("Called loggingControl method")

        if self.enabledCheck.isChecked():
            self.difficultyCheck.setEnabled(True)
            self.errorsCheck.setEnabled(True)
            self.winsCheck.setEnabled(True)
            self.lossesCheck.setEnabled(True)
            self.rollsCheck.setEnabled(True)
            self.bankCheck.setEnabled(True)
            self.methodsCheck.setEnabled(True)
            self.initializationCheck.setEnabled(True)
            self.warningsCheck.setEnabled(True)

        else:
            self.difficultyCheck.setEnabled(False)
            self.errorsCheck.setEnabled(False)
            self.winsCheck.setEnabled(False)
            self.lossesCheck.setEnabled(False)
            self.rollsCheck.setEnabled(False)
            self.bankCheck.setEnabled(False)
            self.methodsCheck.setEnabled(False)
            self.initializationCheck.setEnabled(False)
            self.warningsCheck.setEnabled(False)


class CrapsGame(QMainWindow):
    """A game of craps."""

    def __init__(self, parent=None):
        """Build a game with two dice."""

        super().__init__(parent)
        uic.loadUi(os.path.join('UI Files', 'crapsUI.ui'), self)

        self.actionHelp.triggered.connect(self.help)
        self.actionSettings.triggered.connect(self.settingView)
        self.actionStats.triggered.connect(self.statsView)
        self.actionAchievements.triggered.connect(self.achievementView)
        self.cancelRoll.clicked.connect(self.cancelCurrentRoll)
        self.rollButton.clicked.connect(self.betChangedHandler)
        self.moneyBet.textChanged.connect(self.betVerifier)
        self.cancelRoll.setDisabled(True)

        self.payout = {4: 2, 5: 1.5, 6: 1.2, 8: 1.2, 9: 1.5, 10: 1.2}

        try:
            with open("craps.pkl", 'rb') as pickledData:
                self.pickledSelfData = load(pickledData)
                self.winsCount, self.lossesCount, self.currentBet, self.startingBank, self.currentBank, self.currentRoll, self.secondRoll, self.previousRoll, self.die1, self.die2, self.results, self.betWins, self.betLosses, self.rollAmt, self.preferredDifficultyLevel, self.difficultyLevel, self.minimumBet, self.maximumBet, self.logging, self.difficultyLogging, self.errorsLogging, self.winsLogging, self.lossesLogging, self.rollsLogging, self.bankLogging, self.methodsLogging, self.initializationLogging, self.warningsLogging, self.theme, self.totalGames = self.pickledSelfData
                self.die1.setValue(self.die1.getValue())
                self.die2.setValue(self.die2.getValue())

        except FileNotFoundError:
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
            self.results = "Welcome to the game of Craps!"
            self.betWins = 0
            self.betLosses = 0
            self.rollAmt = 0
            self.preferredDifficultyLevel = 3
            self.difficultyLevel = self.preferredDifficultyLevel
            self.minimumBet = 1
            self.maximumBet = self.currentBank
            self.logging = False
            self.difficultyLogging = False
            self.errorsLogging = False
            self.winsLogging = False
            self.lossesLogging = False
            self.rollsLogging = False
            self.bankLogging = False
            self.methodsLogging = False
            self.initializationLogging = False
            self.warningsLogging = False
            self.theme = "classic"
            self.totalGames = 0

        if self.initializationLogging:
            logging.info("Initialized game app")

    def __str__(self):
        """String representation for Dice"""
        return ""

    def getPreviousRoll(self):
        if self.methodsLogging:
            logging.info("Reached getPreviousRoll method")
        return self.previousRoll

    def setCurrentRoll(self, currentRoll):
        if self.methodsLogging:
            logging.info("Reached setCurrentRoll method")
        self.currentRoll = currentRoll

    def getCurrentRoll(self):
        if self.methodsLogging:
            logging.info("Reached getCurrentRoll method")
        return self.currentRoll

    def setCurrentBank(self, currentBank):
        if self.methodsLogging:
            logging.info("Reached setCurrentBank method")
        self.currentBank = currentBank

    def getCurrentBank(self):
        if self.methodsLogging:
            logging.info("Reached getCurrentBank method")
        return self.currentBank

    def setWinsCount(self, winsCount):
        if self.methodsLogging:
            logging.info("Reached setWinsCount method")
        self.winsCount = winsCount

    def getWinsCount(self):
        if self.methodsLogging:
            logging.info("Reached getWinsCount method")
        return self.winsCount

    def setLossesCount(self, lossesCount):
        if self.methodsLogging:
            logging.info("Reached setLossesCount method")
        self.lossesCount = lossesCount

    def getLossesCount(self):
        if self.methodsLogging:
            logging.info("Reached getLossesCount method")
        return self.lossesCount

    def setCurrentBet(self, currentBet):
        if self.methodsLogging:
            logging.info("Reached setCurrentBet method")
        self.currentBet = currentBet

    def getCurrentBet(self):
        if self.methodsLogging:
            logging.info("Reached getCurrentBet method")
        return self.currentBet

    def setStartingBank(self, startingBank):
        if self.methodsLogging:
            logging.info("Reached setStartingBank method")
        self.startingBank = startingBank

    def getStartingBank(self):
        if self.methodsLogging:
            logging.info("Reached getStartingBank method")
        return self.startingBank

    def placeBet(self, betValue):
        if self.methodsLogging:
            logging.info("Reached placeBet method")
        self.setCurrentBet(betValue)

    def settingView(self):
        if self.methodsLogging:
            logging.info("Reached settingView method")
        settingApp.clearLog.setEnabled(True)
        settingApp.setModal(True)
        settingApp.show()

    def statsView(self):
        if self.methodsLogging:
            logging.info("Reached statsView method")
        statApp.show()

    def achievementView(self):
        if self.methodsLogging:
            logging.info("Reached achievementsView method")
        achievementApp.show()

    def help(self):
        if self.methodsLogging:
            logging.info("Reached help method")
        helpApp.show()

    def changeDifficulty(self, difficulty):
        if self.methodsLogging:
            logging.info("Reached changeDifficulty method")
        self.preferredDifficultyLevel = difficulty

    def saveSettings(self):
        if self.methodsLogging:
            logging.info("Reached saveSettings method")

        self.difficultyLevel = self.preferredDifficultyLevel
        self.startingBank = settingApp.startingBankSpin.value()
        self.minimumBet = settingApp.minimumBetSpin.value()
        self.maximumBet = settingApp.maximumBetSpin.value()

        self.checkOptions = [settingApp.difficultyCheck, settingApp.errorsCheck, settingApp.winsCheck,
                             settingApp.lossesCheck, settingApp.rollsCheck, settingApp.bankCheck,
                             settingApp.warningsCheck, settingApp.initializationCheck, settingApp.methodsCheck]

        if self.difficultyLogging:
            logging.info("Changed difficulty level to " + str(self.difficultyLevel))

        if settingApp.enabledCheck.isChecked():
            self.logging = True
            for checkElement in self.checkOptions:
                if checkElement.isChecked():
                    exec("self." + checkElement.text().lower() + "Logging = True")
                else:
                    exec("self." + checkElement.text().lower() + "Logging = False")
            # print("self.difficultyLogging", self.difficultyLogging)
            # print("self.winsLogging", self.winsLogging)
            # print("self.methodsLogging", self.methodsLogging)
            # print("self.rollsLogging", self.rollsLogging)
            # print("self.errorsLogging", self.errorsLogging)
            # print("self.lossesLogging", self.lossesLogging)
            # print("self.bankLogging", self.bankLogging)
            # print("self.initializationLogging", self.initializationLogging)
            # print("self.warningsLogging", self.warningsLogging)

        else:
            self.logging = False
            for checkElement in self.checkOptions:
                exec("self." + checkElement.text().lower() + "Logging = False")

        self.updateUI()
        settingApp.close()

    def updateUI(self):

        if self.secondRoll:
            self.cancelRoll.setEnabled(True)
            self.hint.setText(
                "You may also choose to not roll again to only lose your placed amount bet without payout ratios.")

        else:
            self.hint.setText("")

        if self.methodsLogging:
            logging.info("Reached updateUI method")

        if self.getCurrentBank() <= 0:
            if self.bankLogging:
                logging.info("Game over")
            self.hint.setText(
                'Game over. You rolled the dice a total of %i times. Go to settings and click restart to play again!' % self.rollAmt)
            self.rollButton.setEnabled(False)
            self.moneyBet.setEnabled(False)

        # self.winsLabel.setText(str(self.getWinsCount()))
        # self.lossesLabel.setText(str(self.getLossesCount()))
        self.resultLabel.setText(self.results)
        self.bank.setText(str("$" + str(self.getCurrentBank())))
        # self.netProfit.setText("$" + str(self.currentBank - self.startingBank))
        # self.profitAmt.setText("$ +" + str(self.betWins))
        # self.lossAmt.setText("$ -" + str(self.betLosses))
        self.die1View.setPixmap(QtGui.QPixmap(":/" + str(self.die1.getValue())))
        self.die2View.setPixmap(QtGui.QPixmap(":/" + str(self.die2.getValue())))

        statApp.totalMoneyWonStat.setText('$' + str(self.betWins))
        statApp.totalMoneyLostStat.setText('$' + str(self.betLosses))
        statApp.totalNetProfitStat.setText('$' + str(self.betWins - self.betLosses))
        statApp.winsStat.setText(str(self.winsCount))
        statApp.lossesStat.setText(str(self.lossesCount))
        statApp.totalRollsStat.setText(str(self.rollAmt))
        statApp.totalGamesPlayedStat.setText(str(self.totalGames))

        if self.winsCount >= 100000:
            achievementApp.tenWins.setText("Achieved")
            achievementApp.hundredWins.setText("Achieved")
            achievementApp.thousandWins.setText("Achieved")
            achievementApp.tenThousandWins.setText("Achieved")
            achievementApp.hundredThousandWins.setText("Achieved")

        elif self.winsCount >= 10000:
            achievementApp.tenWins.setText("Achieved")
            achievementApp.hundredWins.setText("Achieved")
            achievementApp.thousandWins.setText("Achieved")
            achievementApp.tenThousandWins.setText("Achieved")

        elif self.winsCount >= 1000:
            achievementApp.tenWins.setText("Achieved")
            achievementApp.hundredWins.setText("Achieved")
            achievementApp.thousandWins.setText("Achieved")

        elif self.winsCount >= 100:
            achievementApp.tenWins.setText("Achieved")
            achievementApp.hundredWins.setText("Achieved")

        elif self.winsCount >= 10:
            achievementApp.tenWins.setText("Achieved")

        if self.rollAmt >= 100000:
            achievementApp.tenRolls.setText("Achieved")
            achievementApp.hundredRolls.setText("Achieved")
            achievementApp.thousandRolls.setText("Achieved")
            achievementApp.tenThousandRolls.setText("Achieved")
            achievementApp.hundredThousandRolls.setText("Achieved")

        elif self.rollAmt >= 10000:
            achievementApp.tenRolls.setText("Achieved")
            achievementApp.hundredRolls.setText("Achieved")
            achievementApp.thousandRolls.setText("Achieved")
            achievementApp.tenThousandRolls.setText("Achieved")

        elif self.rollAmt >= 1000:
            achievementApp.tenRolls.setText("Achieved")
            achievementApp.hundredRolls.setText("Achieved")
            achievementApp.thousandRolls.setText("Achieved")

        elif self.rollAmt >= 100:
            achievementApp.tenRolls.setText("Achieved")
            achievementApp.hundredRolls.setText("Achieved")

        elif self.rollAmt >= 10:
            achievementApp.tenRolls.setText("Achieved")

        if self.lossesCount >= 100000:
            achievementApp.hundredThousandLosses.setText("Achieved")
            achievementApp.tenThousandLosses.setText("Achieved")
            achievementApp.thousandLosses.setText("Achieved")
            achievementApp.hundredLosses.setText("Achieved")
            achievementApp.tenLosses.setText("Achieved")

        elif self.lossesCount >= 10000:
            achievementApp.tenThousandLosses.setText("Achieved")
            achievementApp.thousandLosses.setText("Achieved")
            achievementApp.hundredLosses.setText("Achieved")
            achievementApp.tenLosses.setText("Achieved")

        elif self.lossesCount >= 1000:
            achievementApp.thousandLosses.setText("Achieved")
            achievementApp.hundredLosses.setText("Achieved")
            achievementApp.tenLosses.setText("Achieved")

        elif self.lossesCount >= 100:
            achievementApp.hundredLosses.setText("Achieved")
            achievementApp.tenLosses.setText("Achieved")

        elif self.lossesCount >= 10:
            achievementApp.tenLosses.setText("Achieved")

        if self.betWins >= 10000000:
            achievementApp.tenMillionBank.setText("Achieved")
            achievementApp.millionBank.setText("Achieved")
            achievementApp.hundredThousandBank.setText("Achieved")
            achievementApp.tenThousandBank.setText("Achieved")
            achievementApp.thousandBank.setText("Achieved")

        elif self.betWins >= 1000000:
            achievementApp.millionBank.setText("Achieved")
            achievementApp.hundredThousandBank.setText("Achieved")
            achievementApp.tenThousandBank.setText("Achieved")
            achievementApp.thousandBank.setText("Achieved")

        elif self.betWins >= 100000:
            achievementApp.hundredThousandBank.setText("Achieved")
            achievementApp.tenThousandBank.setText("Achieved")
            achievementApp.thousandBank.setText("Achieved")

        elif self.betWins >= 10000:
            achievementApp.tenThousandBank.setText("Achieved")
            achievementApp.thousandBank.setText("Achieved")

        elif self.betWins >= 1000:
            achievementApp.thousandBank.setText("Achieved")

    @pyqtSlot()  # player asked for a roll
    def rollAction(self):
        if self.methodsLogging:
            logging.info("Reached rollAction method")

        self.rollAmt += 1

        if self.rollsLogging:
            logging.info("Increased roll amount to {}".format(self.rollAmt))

        self.hint.setText("")

        if self.difficultyLevel == 3:
            self.currentRoll = self.die1.roll(self.difficultyLevel) + self.die2.roll(self.difficultyLevel)
        else:
            self.currentRoll = self.die1.roll(self.difficultyLevel)
            if self.currentRoll < 7:
                self.die1.setValue(random.choice(
                    [x for x in range(1, self.currentRoll)]))  # It's a throwaway variable, so I am using x.
            else:
                self.die1.setValue(random.choice([x for x in range(self.currentRoll - 6, 7)]))
            self.die2.setValue(self.currentRoll - self.die1.getValue())

        if self.rollsLogging:
            logging.info("Rolled {} & {}".format(self.die1.getValue(), self.die2.getValue()))

        self.results = "You rolled a %i and will have to roll again to win money." % (self.currentRoll)
        if self.secondRoll == False:
            if self.rollsLogging:
                logging.info("Rolled a first roll")

            if self.currentRoll == 7 or self.currentRoll == 11:
                if self.winsLogging:
                    logging.info("Won ${}".format(self.getCurrentBet()))

                self.results = "You win $%i!" % self.getCurrentBet()
                self.betWins += self.getCurrentBet()

                self.currentBank += self.getCurrentBet()

                if self.bankLogging:
                    logging.info("Bank amount increased to ${}".format(self.currentBank))

                self.winsCount += 1

                if self.winsLogging:
                    logging.info("Increased wins amount to {}".format(self.winsCount))

            elif self.currentRoll == 2 or self.currentRoll == 3 or self.currentRoll == 12:

                self.results = "You lose $%i!" % self.getCurrentBet()
                self.betLosses += self.getCurrentBet()
                self.lossesCount += 1
                self.currentBank -= self.getCurrentBet()

                if self.bankLogging:
                    logging.info("Lost ${}".format(self.getCurrentBet()))

                if self.lossesLogging:
                    logging.info("Increased losses amount to {}".format(self.lossesCount))
            else:
                self.secondRoll = True
                self.previousRoll = self.currentRoll
                self.hint.setText(
                    "You may also choose to not roll again to only lose your placed amount bet without payout ratios.")
                self.moneyBet.setEnabled(False)
                self.cancelRoll.setEnabled(True)

                if self.rollsLogging:
                    logging.info("Got option to have a second roll")
        else:
            if self.rollsLogging:
                logging.info("Reached second roll")
            if self.previousRoll == self.currentRoll:
                self.winsCount += 1
                self.betAmt = int(self.getCurrentBet() * self.payout[self.getPreviousRoll()])
                self.currentBank += self.betAmt
                self.results = "You win $%i!" % self.betAmt
                self.betWins += self.betAmt

                if self.winsLogging:
                    logging.info("Increased wins amount to {}".format(self.winsCount))

                if self.bankLogging:
                    logging.info("Won ${}".format(self.betAmt))
            else:
                self.lossesCount += 1
                self.betAmt = int(self.getCurrentBet() * self.payout[self.getPreviousRoll()])
                self.currentBank -= self.betAmt
                self.results = "You lose $%i!" % self.betAmt
                self.betLosses += self.betAmt

                if self.lossesLogging:
                    logging.info("Increased losses amount to {}".format(self.winsCount))

                if self.bankLogging:
                    logging.info("Lost ${}".format(self.betAmt))

            self.moneyBet.setEnabled(True)
            self.cancelRoll.setEnabled(False)
            self.secondRoll = False
        self.updateUI()

    def betVerifier(self):
        if self.methodsLogging:
            logging.info("Reached betVerifier method")
        try:
            moneyBet = int(self.moneyBet.toPlainText())
            if moneyBet <= 0:
                self.results = "You cannot bet with amounts less than 0 or 0 itself."
                self.rollButton.setEnabled(False)

            elif moneyBet > self.maximumBet:
                self.results = "This bet of ${} is too high. Please change your settings or reduce ${} from your bet.".format(
                    moneyBet, moneyBet - self.maximumBet)
                self.rollButton.setEnabled(False)

            elif moneyBet < self.minimumBet:
                self.results = "This bet of ${} is too low. Please change your settings or add ${} to your bet.".format(
                    moneyBet, self.minimumBet - moneyBet)
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

    @pyqtSlot()  # player clicking the roll button
    def betChangedHandler(self):
        settingApp.restartButton.setEnabled(True)
        if self.methodsLogging:
            logging.info("Reached betChangedHandler method")
        try:
            moneyBet = int(self.moneyBet.toPlainText())
            # if self.getCurrentBank() <= 0:
            #     self.results = "Game over. You rolled the dice a total of %i times." % self.rollAmt
            #     self.hint.setText('Click restart to play again!')
            #     self.rollButton.setEnabled(False)
            #     self.moneyBet.setEnabled(False)
            # elif moneyBet <= 0:
            #     self.results = "You cannot bet with amounts less than 0 or 0 itself."
            #     self.rollButton.setEnabled(False)

            if moneyBet > self.maximumBet:
                self.results = "This bet of {} is too high. Please change your settings or reduce ${} from your bet and retype your bet.".format(
                    moneyBet, moneyBet - self.maximumBet)
                self.rollButton.setEnabled(False)
                self.updateUI()
                return

            if moneyBet < self.minimumBet:
                self.results = "This bet of {} is too low. Please change your settings or add ${} to your bet and retype your bet.".format(
                    moneyBet, self.minimumBet - moneyBet)
                self.rollButton.setEnabled(False)
                self.updateUI()
                return

            if moneyBet <= self.getCurrentBank():
                self.setCurrentBet(int(self.moneyBet.toPlainText()))
                self.rollAction()
            else:
                self.results = "Error, you cannot bet with what you do not have. Please try again."
                self.rollButton.setEnabled(False)

        except:
            print(self.moneyBet.toPlainText())
            self.results = "Please type in an integer as a bet."
            self.rollButton.setEnabled(False)
        self.updateUI()

    def cancelCurrentRoll(self):
        if self.methodsLogging:
            logging.info("Reached cancelCurrentRoll method")

        self.currentBank -= self.currentBet
        self.results = "You have decided to not roll and have lost your initial bet amount of $%i." % self.getCurrentBet()
        self.hint.setText("")
        self.betLosses += self.currentBet
        self.secondRoll = False
        self.updateUI()
        self.cancelRoll.setEnabled(False)
        self.moneyBet.setEnabled(True)

        if self.rollsLogging:
            logging.info("Did not reach second roll")

        if self.bankLogging:
            logging.info("Lost ${}".format(self.currentBet))

    def restart(self):
        if self.methodsLogging:
            logging.info("Reached restart method")

        self.startingBank = settingApp.startingBankSpin.value()
        # self.winsCount = 0
        # self.lossesCount = 0
        self.currentBet = 10
        self.currentBank = self.startingBank
        self.currentRoll = 0
        self.secondRoll = False
        self.previousRoll = 0
        self.results = "You have restarted the game."
        self.moneyBet.setEnabled(True)
        self.hint.setText("")
        self.rollButton.setEnabled(True)
        self.cancelRoll.setEnabled(False)
        # self.betWins = 0
        # self.betLosses = 0
        # self.rollAmt = 0
        self.totalGames += 1
        self.updateUI()

        settingApp.restartButton.setEnabled(False)

    def deleteLog(self):
        open("craps.log", 'w').close()
        logging.info("Cleared log")
        settingApp.clearLog.setEnabled(False)

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit Craps? All changes will be saved."
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        self.pickleInfo = [self.winsCount, self.lossesCount, self.currentBet, self.startingBank, self.currentBank,
                           self.currentRoll, self.secondRoll, self.previousRoll, self.die1, self.die2, self.results,
                           self.betWins, self.betLosses, self.rollAmt, self.preferredDifficultyLevel,
                           self.difficultyLevel, self.minimumBet, self.maximumBet, self.logging, self.difficultyLogging,
                           self.errorsLogging, self.winsLogging, self.lossesLogging, self.rollsLogging,
                           self.bankLogging, self.methodsLogging, self.initializationLogging, self.warningsLogging,
                           self.theme, self.totalGames]

        if reply == QMessageBox.Yes:
            event.accept()
            with open("craps.pkl", 'wb') as crapsPickle:
                dump(self.pickleInfo, crapsPickle)
            exit()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    logging.basicConfig(filename='craps.log',
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)s Ln %(lineno)d: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    crapsApp = CrapsGame()
    helpApp = HelpWindow()
    statApp = AppStats()
    achievementApp = AchievementWindow()
    settingApp = AppSettings()
    crapsApp.updateUI()
    crapsApp.show()
    sys.exit(app.exec_())
