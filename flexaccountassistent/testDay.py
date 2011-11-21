'''
Created on 27/10/2011

@author: Antek
'''
from datetime import time
import unittest
from flexaccountassistent import day
from flexaccountassistent.day import Day, timeToMinutes, DictionaryDayService
import datetime

#from flexaccounassistent import day
#from flexaccounassistent.day import Day, timeToMinutes




class TestRoundTime(unittest.TestCase):
    def testRoundDown(self):
        """Should round down when remnant from minutes is less than 5"""
        t = time(8, 22)
        expected = time(8, 20)
        self.assertEqual(day.roundTime(t).minute, expected.minute)
        
    def testRoundUp(self):
        """Should round up when remnant from minutes is less than 5"""
        t = time(8, 26)
        expected = time(8, 30)
        self.assertEqual(day.roundTime(t).minute, expected.minute)
        
    def testRoundUpWithHourChange(self):
        """Should round down when remnant from minutes is less than 5"""
        t = time(8, 56)
        expected = time(9, 0)
        self.assertEqual(day.roundTime(t).minute, expected.minute)
        
class TestDay(unittest.TestCase):
    monday = datetime.date(2011, 11, 07)
    tuesday = datetime.date(2011, 11, 8)
    friday = datetime.date(2011, 11, 11)
#    def __init__(self):
#        unittest.TestCase.__init__(self)
#        self.monday = datetime.date(2011, 11, 07) #A Monday
        
    def testCountTime(self):
        d = Day(date = TestDay.monday)
        d.setStop(time(16, 20))
        expected = time(7, 30)
        self.assertEqual(d.countTime(), timeToMinutes(expected)) 
        
    def testCountTimeNoPause(self):
        d = Day(date = TestDay.monday, pause = 0)
        d.setStop(time(16, 20))
        expected = time(8, 0)
        self.assertEqual(d.countTime(), timeToMinutes(expected)) 
    
    def testNoEndTimeSet(self):
        d = Day(date = TestDay.monday, pause = 0)
        try:
            d.countTime()
        except AttributeError:
            pass
    
    def testWithStartTime(self):
        d = Day(date = TestDay.monday, startTime = time(8, 0))
        d.setStop(time(16, 00))
        expected = time (7, 30)
        self.assertEqual(d.countTime(), timeToMinutes(expected)) 
        
    def testTypeNormal(self):
        d = Day(TestDay.monday)
        self.assertEqual(d.workingMinutes, Day.NORMAL_HOURS * Day.MINUTES_IN_HOUR)
        
class TestDayDictionaryService(unittest.TestCase):
    
    def testInint(self):
        dictionaryService = DictionaryDayService(600)
        self.assertEqual(dictionaryService.getBalance(), 600)
        
    def testOneDay(self):
        dictionaryService = DictionaryDayService(600)
        d = Day(date = TestDay.monday)
        d.setStop(time(17, 20))
        dictionaryService.addDay(d)
        self.assertEqual(dictionaryService.getBalance(), 660)
        
    def testTwoDays(self):
        dictionaryService = DictionaryDayService(600)
        d = Day(date = TestDay.monday)
        d.setStop(time(17, 20))
        dictionaryService.addDay(d)
        d = Day(date = TestDay.tuesday)
        d.setStop(time(17, 20))
        dictionaryService.addDay(d)
        self.assertEqual(dictionaryService.getBalance(), 720)
        
    def testThreeDaysWithFriday(self):
        dictionaryService = DictionaryDayService(600)
        d = Day(date = TestDay.monday)
        d.setStop(time(17, 20))
        dictionaryService.addDay(d)
        d = Day(date = TestDay.tuesday)
        d.setStop(time(17, 20))
        dictionaryService.addDay(d)
        d = Day(date = TestDay.friday)
        d.setStop(time(17, 20))
        dictionaryService.addDay(d)
        self.assertEqual(dictionaryService.getBalance(), 810)
        
    def testThreeDaysWithMinus(self):
        dictionaryService = DictionaryDayService(50)
        d = Day(date = TestDay.monday)
        d.setStop(time(14, 20))
        dictionaryService.addDay(d)
        d = Day(date = TestDay.tuesday)
        d.setStop(time(14, 20))
        dictionaryService.addDay(d)
        d = Day(date = TestDay.friday)
        d.setStop(time(14, 20))
        dictionaryService.addDay(d)
        self.assertEqual(dictionaryService.getBalance(), -280)
        
        
   
