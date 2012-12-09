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

import os, pickle, tempfile as tmp

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
    
class StatusTest(unittest.TestCase):
    def test_status_without_init_rises_exception(self):
        try:
            status()
            self.fail()
        except IOError:
            pass
        
        
class TestWithDBMock(object):
    def setUp(self):
        self.tmpdir = tmp.mkdtemp()
        print(self.tmpdir)
        self.DB = FlexAccountDB(self.tmpdir)
    def tearDown(self):
        os.remove(self.DB.getDataFilePath())
        os.rmdir(self.tmpdir)  
 
    
class AddTest(TestWithDBMock, unittest.TestCase):
    def _performTest(self, initial, toAdd, toCompare):
        init(self.DB, initial)
        add(self.DB, toAdd)
        self.assertEqual(toCompare, status(self.DB))

    def test_add_with_positive_gives_correct_result(self):
        initial = TimeCalculations(2, 15)
        toAdd = TimeCalculations(1, 55)
        toCompare = TimeCalculations(4, 10)
        self._performTest(initial, toAdd, toCompare)

    def test_add_with_negative_gives_correct_result(self):
        initial = TimeCalculations(1, 55)
        toAdd = TimeCalculations(2, 15, -1)
        toCompare = TimeCalculations(0, 20, -1)
        self._performTest(initial, toAdd, toCompare)

            
class InterfaceFunctionTest(TestWithDBMock, unittest.TestCase):

    def test_status_returns_correct_value(self):
        toCompare = TimeCalculations(2, 15)
        init(self.DB, toCompare)
        self.assertEqual(toCompare, status(self.DB))
        

    
class TimeCalculationCreationTest(unittest.TestCase):
    def test_format_has_two_numbers_separated_with_a_colon(self):
        time1 = TimeCalculations(2, 15)
        self.assertTrue(time1, createTimeCalculation('2:15'))
    
    def test_lack_of_colon_raises_excpetion(self):
        self.__performTest('215')
    def test_lack_of_hours_raises_excpetion(self):
        self.__performTest(':15')
        
    def test_lack_of_minutes_raises_excpetion(self):
        self.__performTest('2:')
    
    def test_minutes_with_minus_raise_excpetion(self):
        self.__performTest('2:-15')
    
    def test_incorrect_amount_of_hours_raises_excpetion(self):
        self.__performTest('2a:0')
    
    def test_incorrect_amount_of_minutes_raises_excpetion(self):
        self.__performTest('2:a0')
    
    def __performTest(self, toTest):
        try:
            createTimeCalculation(toTest)
        except ValueError:
            pass
        
        except SyntaxError:
            pass
        
        else:
            self.fail()     
        

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