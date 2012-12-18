'''
Created on 08/07/2012
This version of FlexAccountAssistent only registers the difference between worked time and
the planned time.
@author: Antek
'''
import unittest

def timeCalculationsWithDifferentSign(timeCalculations):
    toReturn = TimeCalculations(timeCalculations.hours, timeCalculations.minutes)
    if timeCalculations.sign == 1:
        toReturn.sign = -1
    return toReturn        
        
class TimeCalculations(object):
    ''' Holds amount of hours and minutest and allows to perform basic arithmetical operations.'''
    def __init__(self, hours, minutes, sign = 1):
        
        if not self.__checkValues(hours, minutes, sign):
            raise ValueError
        
        self.hours = hours
        self.minutes = minutes
        self.sign = sign
    
    def __eq__(self, other):
        
        if self.__class__ != other.__class__:
            return False
        
        return self.sign == other.sign and self.hours == other.hours and self.minutes == other.minutes
    
    def __ge__(self, other):
        if self.sign < other.sign:
            return False
        if self.hours >= other.hours:
            return True
        else:
            return self.minutes >= other.minutes

    def __checkSign(self, sign):
        return sign == 1 or sign == -1
    
    def __checkHours(self, hours):
        return hours >= 0
    
    def __checkMinutes(self, minutes):
        return minutes >= 0 and minutes <= 59
    
    def __checkValues(self, hours, minutes, sign):
        
        hoursCorrect = self.__checkHours(hours) 
        minutesCorrect = self.__checkMinutes(minutes)
        signCorrect = self.__checkSign(sign)
        
        return  hoursCorrect and minutesCorrect and signCorrect  
        
    def convertToMinutes(self):
        return self.sign * (self.hours * 60 + self.minutes)
    
    def add(self, other):
        selfConverted = self.convertToMinutes()
        otherConverted = other.convertToMinutes() 
        resultConverted = selfConverted + otherConverted
        resultSign = getSign(resultConverted)
        resultConverted *= resultSign 

        return TimeCalculations(resultConverted / 60, resultConverted % 60, resultSign)

            
            
    
    def subtract(self, toSubtract):
        withChangedSign = TimeCalculations(toSubtract.hours, toSubtract.minutes, toSubtract.sign * -1)
        return self.add(withChangedSign)


def getSign(number):
    if number >= 0:
        return 1
    else:
        return -1


    
def createTimeCalculation(toConvert):
    """Creates a TimeCalculation form a string
    that is in the following format signHH:MM"""
    splited = toConvert.partition(':')
    if splited.__len__() != 3:
        raise ValueError
    hours = int(splited[0])
    minutes = int(splited[2])
    if minutes < 0:
        raise ValueError
    sign = getSign(hours)
    hours *= sign
    return TimeCalculations(hours, minutes, sign)

import os, pickle

_HOME_DIR = '~'
_DIR_NAME = '.faa'

def getDefaultPath():
    return os.path.join(os.path.expanduser(_HOME_DIR), _DIR_NAME)
    
class FlexAccountDB(object):
    def __init__(self, dbfile=getDefaultPath(), fileName ='faa.dat'):
        self.dbfile = dbfile    
        self.fileName = fileName    
    def getDataFilePath(self):
        #print(os.path.join(self.dbfile, self.fileName))
        return os.path.join(self.dbfile, self.fileName)
    def getDataFile(self, mode = 'w'):
        if not os.path.exists(self.dbfile):
            os.makedirs(self.dbfile)    
        return open(self.getDataFilePath(), mode)
    


def init(dbase = FlexAccountDB(),  initial = None):
    '''Initializes the database.'''
    dataFile = dbase.getDataFile('w')
    
    if initial == None:
        initial = TimeCalculations(0, 0)
    pickle.dump(initial, dataFile, pickle.HIGHEST_PROTOCOL) 

def status(dbase = FlexAccountDB()):
    '''Returns the value of the flex account'''
    dataFile = dbase.getDataFile('r')
    return pickle.load(dataFile)
    
def add(toAdd, dbase = FlexAccountDB()):
    present = status(dbase)
    init(dbase, present.add(toAdd))