'''
Created on 18/12/2012

@author: Antek
'''
from flexaccountassistent.flexAccountAssistent import TimeCalculations,\
    FlexAccountDB, init, add, status, createTimeCalculation
import os.path
import unittest
import tempfile as tmp


class TestWithDBMock(object):
    def setUp(self):
        self.tmpdir = tmp.mkdtemp()
        print(self.tmpdir)
        self.DB = FlexAccountDB(self.tmpdir)
    def tearDown(self):
        repoPath = self.DB._getDataFilePath()
        if os.path.exists(repoPath):
            os.remove(repoPath)
        os.rmdir(self.tmpdir)  

class StatusTest(TestWithDBMock, unittest.TestCase):
    def test_status_without_init_rises_exception(self):
        try:
            status(self.DB)
            self.fail()
        except IOError:
            pass
         
    
class AddTest(TestWithDBMock, unittest.TestCase):
    def _performTest(self, initial, toAdd, toCompare):
        init(self.DB, initial)
        add(toAdd, self.DB)
        self.assertEqual(toCompare, status(self.DB).timeCalculations)

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
        self.assertEqual(toCompare, status(self.DB).timeCalculations)
        

    
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