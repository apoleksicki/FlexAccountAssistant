'''
Created on 29/11/2011

@author: Antek
'''
from flexaccountassistent.day import DictionaryDayService

welcomeText = u"Flex Account Assistent"
makeDecision = u"Make you decision"
addDay = u"1. Add day"
viewFlexAccount = u"2. View flex account"
createNowAccount = u"3."
exit = u"0. Exit program"

valueErrorMsg = u"Wrong value"


def printMenu():
    print welcomeText
    print makeDecision
    print addDay
    print viewFlexAccount
    print exit

def printValueErrorMsg():
    
    print valueErrorMsg
    
EXIT = 0
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
                print service.getBalance()
                 
        except EOFError:
            break
        except ValueError:
            printValueErrorMsg()
            
            