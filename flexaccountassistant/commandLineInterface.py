'''
Created on 11/07/2012
Provides a console interface to deal with 
@author: Antek
'''
import argparse, flexAccountAssistant as faa
import logging, os

if __name__ == '__main__':
    logging.basicConfig(filename=os.path.join(faa.getDefaultPath(), 'faa.log'),format='%(asctime)s %(message)s', level=logging.DEBUG)
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
            print faa.status()
        except IOError:
            print "The flex account assistent hasn't been initialised. Please run init." 
    elif operation == CHOICES[2] or operation == CHOICES[3]:
        timeCalc = faa.createTimeCalculation(time)
        if operation == CHOICES[3]:
            timeCalc = faa.timeCalculationsWithDifferentSign(timeCalc)
        faa.add(timeCalc)
    elif operation == CHOICES[4]:
        timeCalc = faa.createTimeCalculation(time)
        faa.init(timeCalc)
   
   
        

        