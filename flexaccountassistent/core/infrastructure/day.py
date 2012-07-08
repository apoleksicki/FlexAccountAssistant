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
    
    def __getSign(self, number):
        if number >= 0:
            return 1
        else:
            return -1


    def add(self, other):
        selfConverted = self.convertToMinutes()
        otherConverted = other.convertToMinutes() 
        resultConverted = selfConverted + otherConverted
        resultSign = self.__getSign(resultConverted)
        resultConverted *= resultSign 

        return TimeCalculations(resultConverted / 60, resultConverted % 60, resultSign)

            
            
    
    def subtract(self, toSubtract):
        withChangedSign = TimeCalculations(toSubtract.hours, toSubtract.minutes, toSubtract.sign * -1)
        return self.add(withChangedSign)
    
    
class TimeCalculationsTest(unittest.TestCase):
    
    def test_when_adding_positive_to_positive_result_is_positive(self):
        time1 = TimeCalculations(2, 15)
        time2 = TimeCalculations(1, 55)
        expected = TimeCalculations(4, 10)
        self.assertTrue(expected == time1.add(time2))
        
    def test_adding_negative_to_negative_is_negative(self):
        time1 = TimeCalculations(2, 15)
        time2 = TimeCalculations(1, 55)
        expected = TimeCalculations(4, 10)
        self.assertEqual(expected, time1.add(time2))
        
    def test_when_adding_positive_to_negative_result_is_positive_when_positive_is_greater(self):
        time1 = TimeCalculations(2, 15, -1)
        time2 = TimeCalculations(1, 55, -1)
        expected = TimeCalculations(4, 10, -1)
        self.assertEqual(expected, time1.add(time2))
        
    def test_when_adding_positive_to_negative_result_is_negative_when_negative_is_greater(self):
        time1 = TimeCalculations(1, 55)
        time2 = TimeCalculations(2, 15, -1)
        expected = TimeCalculations(0, 20, -1)
        self.assertEqual(expected, time1.add(time2))

        
    def test_when_adding_negative_to_positive_result_is_positive_when_positive_is_greater(self):
        time1 = TimeCalculations(2, 15, -1)
        time2 = TimeCalculations(1, 55, -1)
        expected = TimeCalculations(4, 10, -1)
        self.assertEqual(expected, time1.add(time2))
        
    def test_when_adding_negative_to_positive_result_is_negative_when_negative_is_greater(self):
        time1 = TimeCalculations(2, 15, -1)
        time2 = TimeCalculations(1, 55, 1)
        expected = TimeCalculations(0, 20, -1)
        self.assertEqual(expected, time2.add(time1))

        
    def test_subtracting_negative_from_negative_acts_like_adding(self):
        time1 = TimeCalculations(2, 15, -1)
        time2 = TimeCalculations(1, 55, -1)
        expected = TimeCalculations(0, 20, -1)
        self.assertEqual(expected, time1.subtract(time2))
        
    def test_when_subtracting_positive_from_negative_result_is_negative(self):
        time1 = TimeCalculations(2, 15, -1)
        time2 = TimeCalculations(1, 55, 1)
        expected = TimeCalculations(4, 10, -1)
        self.assertEqual(expected, time1.subtract(time2))
        
    def test_when_subtracting_negative_from_postive_result_is_positive(self):
        time1 = TimeCalculations(2, 15, 1)
        time2 = TimeCalculations(1, 55, -1)
        expected = TimeCalculations(4, 10)
        self.assertEqual(expected, time1.subtract(time2))
        
    def test_when_subtracting_postive_from_positive_result_is_positive_when_first_is_greater(self):
        time1 = TimeCalculations(2, 15, 1)
        time2 = TimeCalculations(1, 55, 1)
        expected = TimeCalculations(0, 20, 1)
        self.assertEqual(expected, time1.subtract(time2))
        
    def test_when_subtracting_positive_from_positive_result_is_negative_when_second_is_greater(self):
        time1 = TimeCalculations(2, 15, 1)
        time2 = TimeCalculations(1, 55, 1)
        expected = TimeCalculations(0, 20, -1)
        self.assertEqual(expected, time2.subtract(time1))
    
    def test_sign_can_be_only_one_or_minus_one(self):
        try:
            TimeCalculations(0, 0, 15)
            self.assertTrue(False)
        except ValueError:
            pass
        else:
            self.fail("Sign can be only 1 or -1")
    
    def test_amount_of_minutest_can_be_between_0_and_59(self):
        try:
            TimeCalculations(0, 100)
            self.assertTrue(False)
        except ValueError:
            pass
        else:
            self.fail("Minutes can be only between 0 and 59")
        
    
    def test_amount_of_hours_has_to_be_greater_than_zero(self):
        try:
            TimeCalculations(-12, 0, 0)
            self.assertTrue(False)
        except ValueError:
            pass
        else:
            self.fail("Amount of hours has to be equals or higher than 0")
        
        
        
     
        
