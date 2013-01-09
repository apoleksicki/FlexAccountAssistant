'''
Created on 11/07/2012
Provides a console interface to deal with 
@author: Antek
'''
import argparse, flexAccountAssistant as faa
import logging, os

CHOICES = ['init', 'status', 'add', 'subtract', 'adjust']

def init(args):
    faa.init()

def status(args):
    print faa.status()
    
def add(args):
    faa.add(faa.createTimeCalculation(args.time))
    
def sub(args):
    timeCalc = faa.createTimeCalculation(args.time)
    timeCalc = faa.timeCalculationsWithDifferentSign(timeCalc)
    faa.add(timeCalc)

def setTime(args):
    faa.init(initial=faa.createTimeCalculation(args.time))
    
def _createParser():
    parser = argparse.ArgumentParser(description='Helps to follow changes on your flex account.')
    subparsers = parser.add_subparsers(help='Possible options:')
    initParser = subparsers.add_parser('init', help='Initialises Flex Account Assistant')
    initParser.set_defaults(func=init)
    
    statusParser = subparsers.add_parser('status', help='Shows the status.')
    statusParser.set_defaults(func=status)
    
    addParser = subparsers.add_parser('add', help='Adds a value to your status.')
    addParser.set_defaults(func=add)
    addParser.add_argument('time', help='Time you want to add in hh:mm format.')
    
    subParser = subparsers.add_parser('sub',  help='Subtracts a value to your status.')
    subParser.set_defaults(func=sub)
    subParser.add_argument('time', help='Time you want to subtract in hh:mm format.')
       
    setParser = subparsers.add_parser('set',  help='Sets the status to the given value.')
    setParser .set_defaults(func=setTime)
    setParser .add_argument('time', help='Time you want to set in hh:mm format. Negative values have to be preceded by \'--\'. ')
       
    return parser

if __name__ == '__main__':
    logging.basicConfig(filename=os.path.join(faa.getDefaultPath(), 'faa.log'),format='%(asctime)s %(message)s', level=logging.DEBUG)
    args = _createParser().parse_args()
    args.func(args)

   
   
        

        