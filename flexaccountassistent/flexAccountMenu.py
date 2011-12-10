'''
Created on 29/11/2011

@author: Antek
'''

welcomeText = u"Flex Account Assistent"
makeDecision = u"Make you decision"
addDay = u"1. Add day"
viewFlexAccount = u"2. View flex account"
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

if __name__ == "__main__":
    choice = 100
    while choice != 0:
        printMenu()
        try:
            choice = int(raw_input("Your choice: "))
        except EOFError:
            break
        except ValueError:
            printValueErrorMsg()
            
            