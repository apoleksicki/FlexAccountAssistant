'''
Created on 29/11/2011

@author: Antek
'''
from flexaccountassistent.core.infrastructure.day import  Day
from datetime import time
from flexaccountassistent.core.service.dayService import DictionaryDayService

welcomeText = u"Flex Account Assistent"
makeDecisionText = u"Make you decision"
addDayText = u"1. Add day"
viewFlexAccountText = u"2. View flex account"
createNowAccountText = u"3."
exitText = u"0. Exit program"

valueErrorMsg = u"Wrong value"


def printMenu():
    print welcomeText
    print makeDecisionText
    print addDayText
    print viewFlexAccountText
    print exitText


def readTime(message):
    timeToParse = raw_input(message)
    splited = timeToParse.split(':')
    hours = int(splited[0])
    minutes = int(splited[1]) 
    return time(hours, minutes)

def createDay():
    infoMessage = 'Adding a new day'
    startTimeMessage = 'Give start time \'HH:MM\':'
    pauseMessage = 'Give pause:'
    endTimeMessage = 'Give end time \'HH:MM\':'
    
    print infoMessage
    startTime = readTime(startTimeMessage)
    endTime = readTime(endTimeMessage)
    pause = int(raw_input(pauseMessage))
    toReturn = Day(pause=pause, startTime=startTime)
    toReturn.setStop(endTime)
    return toReturn

def printValueErrorMsg():
    print valueErrorMsg
    
def showBalance(service):
    balanceInMinutes = service.getBalance()
    hours = balanceInMinutes / 60
    minutes = balanceInMinutes % 60
    print 'Balance: %i:%i' % (hours, minutes)
    
EXIT = 0
ADD_DAY = 1
VIEW_BALANCE = 2
NEW_ACCOUNT = 3
service = None
if __name__ == "__main__":
    choice = 100
    service = DictionaryDayService()
    while choice != EXIT:
        printMenu()
        try:
            choice = int(raw_input("Your choice: "))
            if choice == VIEW_BALANCE:
                showBalance(service)
            elif choice == ADD_DAY:
                day = createDay()
                service.addDay(day)
            elif choice == EXIT:
                service.close()
                 
        except EOFError:
            break
        except ValueError:
            printValueErrorMsg()
            
            