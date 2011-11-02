'''
Created on 27/10/2011

@author: Antek
'''
from datetime import time
import unittest

from flexaccounassistent import day
from flexaccounassistent.day import Day




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
    def testCountTime(self):
        d = Day()
        d.setStop(time(16, 20))
        expected = time(7, 30)
        self.assertEqual(d.countTime(), expected) 
        
    def testCountTimeNoPause(self):
        d = Day(pause = 0)
        d.setStop(time(16, 20))
        expected = time(8, 0)
        self.assertEqual(d.countTime(), expected) 
    
    def testNoEndTimeSet(self):
        d = Day(pause = 0)
        expected = time(8, 0)
        try:
            d.countTime()
        except AttributeError:
            pass
        
        
   
