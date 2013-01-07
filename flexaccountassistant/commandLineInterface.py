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

def _createParser():
    parser = argparse.ArgumentParser(description='Helps to follow changes on you flex account.')
#    parser.add_argument('operation', choices=CHOICES, nargs=2, metavar=('bar', 'baz'))
#    parser.add_argument('--time')
    parser.add_argument('--foo', action='store_true', help='foo help')
    subparsers = parser.add_subparsers(help='sub-command help')
    initParser = subparsers.add_parser('init', help='inits faa')
    initParser.set_defaults(func=init)
    
    statusParser = subparsers.add_parser('status', help='Shows the status')
    statusParser.set_defaults(func=status)
    
    
    parser_a = subparsers.add_parser('a', help='a help')
    parser_a.add_argument('bar', type=int, help='bar help')
    
    parser_b = subparsers.add_parser('b', help='b help')
    parser_b.add_argument('--baz', choices='XYZ', help='baz help')
    
    return parser

def getArguments():
    return 'add 2'.split()

#foo = _createParser()
#foo.parse_args('add 2:30'.split())

if __name__ == '__main__':
    logging.basicConfig(filename=os.path.join(faa.getDefaultPath(), 'faa.log'),format='%(asctime)s %(message)s', level=logging.DEBUG)

    

    args = _createParser().parse_args()
    args.func(args)
#    if args. != None:
#        print 'foo bar baz'
#    operation = args.operation
#    time = args.time
#    
#    if operation == CHOICES[0]:
#        timeCalc = None
#        if (time != None):
#            timeCalc = faa.createTimeCalculation(time)
#        faa.init(initial=timeCalc)
#    elif operation == CHOICES[1]:
#        try:
#            print faa.status()
#        except IOError:
#            print "The flex account assistent hasn't been initialised. Please run init." 
#    elif operation == CHOICES[2] or operation == CHOICES[3]:
#        timeCalc = faa.createTimeCalculation(time)
#        if operation == CHOICES[3]:
#            timeCalc = faa.timeCalculationsWithDifferentSign(timeCalc)
#        faa.add(timeCalc)
#    elif operation == CHOICES[4]:
#        timeCalc = faa.createTimeCalculation(time)
#        faa.init(timeCalc)
   
   
        

        