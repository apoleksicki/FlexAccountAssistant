u'''
Created on 24/10/2011

@author: Antek
'''

import datetime
import unittest
from datetime import time

def roundTime(timeToRound):
    u"""rounds time five minuter up or down"""
    roundedMinute = 0
    roundedHour = timeToRound.hour
    
    if timeToRound.minute % 10 <= 5:
        roundedMinute = timeToRound.minute / 10 * 10
       
    if timeToRound.minute % 10 > 5:
        roundedMinute = (timeToRound.minute / 10 + 1) * 10
        if roundedMinute > 50:
            roundedHour += 1
            roundedMinute = 0
       
    return time(roundedHour, roundedMinute)
  
def timeToMinutes(t):
    return t.hour * 60 + t.minute 
  

class Day(object):
    '''
import unittest
import unittest
import unittest
    Class that represents a working day.
    '''
    NORMAL = 0
    HOLIDAY = 1 
    MINUTES_IN_HOUR = 60
    NORMAL_HOURS = 7.5
    FRIDAY_HOURS = 7
    
    DATE = 0
    PAUSE = 1
    START_TIME = 2
    DAY_TYPE = 3
    END_TIME = 4

    def __init__(self, date=None, pause=30, startTime=None, dayType = NORMAL):
        '''
        Constructor
        '''
        object.__init__(self)
        if date == None:
            self.date = datetime.date.today()
        else:
            self.date = date
        if startTime == None:
            self.startTime = time(8, 20)
        else:
            self.startTime = startTime
            
        if dayType == Day.NORMAL:
            if self.date.isoweekday() < 5:
                self.workingMinutes = Day.NORMAL_HOURS * Day.MINUTES_IN_HOUR
            elif self.date.isoweekday() == 5:
                self.workingMinutes = Day.FRIDAY_HOURS * Day.MINUTES_IN_HOUR 
            else:
                self.workingMinutes = 0 
        else:
            self.workingMinutes = 0
                
        self._dayType = dayType     
        self.pause = pause
        self.endTime = None
        
        
    def setStop(self, endTime = datetime.datetime.now()):
        self.endTime = endTime
        
    def countTime(self):
        

        startTimeStamp = timeToMinutes(self.startTime)
        try:
            endTimeStamp = timeToMinutes(self.endTime)
        except:
            raise AttributeError("setStop has not been called")
            
        workedMinutes = endTimeStamp - startTimeStamp - self.pause
        
        return workedMinutes
        



class SimplifiedDay(object):
    
    '''SimplifiedDay is a container class, that contains only work time on a particular date.'''
    
    def __init__(self, hours, minutes, date=None):
        self.hours = hours
        self.minutes = minutes 
        self.date = date 
        
class TimeCalculations(object):
    ''' Holds amount of hours and minutest and allows to perform basic arithmetical operations.'''
    def __init__(self, hours, minutes):
        self.hours = hours
        self.minutes = minutes
    
    def add(self, toAdd):
        pass
    
    def subtract(self, toSubtract):
        pass
    
    
class TimeCalculationsTest(unittest.TestCase):
    def test_when_adding_positive_to_positive_result_is_positive(self):
        pass
    
    def test_adding_negative_to_negative_is_negative(self):
        pass
        
    def test_when_adding_positive_to_negative_result_is_positive_when_positive_is_greater(self):
        pass
        
    def test_when_adding_positive_to_negative_result_is_negative_when_negative_is_greater(self):
        pass
        
    def test_when_adding_negative_to_positive_result_is_positive_when_positive_is_greater(self):
        pass
        
    def test_when_adding_negative_to_positive_result_is_negative_when_negative_is_greater(self):
        pass
        
    def test_subtracting_negative_from_negative_is_negative(self):
        pass
        
    def test_when_subtracting_positive_from_negative_result_is_negative(self):
        pass
        
    def test_when_subtracting_negative_from_postive_result_positive(self):
        pass
        
    def test_when_subtracting_postive_from_positive_result_is_positive_when_first_is_greater(self):
        pass
        
    def test_when_subtracting_positive_from_positive_result_is_negative_when_second_is_greater(self):
        pass
        
        
        
     
        
