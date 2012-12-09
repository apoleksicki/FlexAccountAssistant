'''
Created on 11/07/2012
Provides a console interface to deal with 
@author: Antek
'''
import argparse, flexAccountAssistent as faa

def timeCalcToString(toParse):
    sign = ''
    if (toParse.sign == -1):
        sign = '-'
    print '%s%2d:%2d' % (sign, toParse.hours, toParse.minutes)  

if __name__ == '__main__':
    CHOICES = ['init', 'status', 'add', 'subtract', 'adjust']
    parser = argparse.ArgumentParser(description='Helps to follow changes on you flex account.')
    parser.add_argument('operation', choices=CHOICES)
    parser.add_argument('--time')

    

    args = parser.parse_args()
    operation = args.operation
    time = args.time
    
    if operation == CHOICES[0]:
        timeCalc = None
        if (time != None):
            timeCalc = faa.createTimeCalculation(time)
        faa.init(initial=timeCalc)
    elif operation == CHOICES[1]:
        try:
            timeCalcToString(faa.status())
        except IOError:
            print "The flex account assistent hasn't been initialised. Please run init." 
    elif operation == CHOICES[2] or CHOICES[3]:
        timeCalc = faa.createTimeCalculation(time)
        if operation == CHOICES[3]:
            timeCalc = faa.timeCalculationsWithDifferentSign(timeCalc)
        faa.add(timeCalc)
    elif operation == CHOICES[4]:
        timeCalc = faa.createTimeCalculation(time)
        faa.init(timeCalc)
   
   
        

        