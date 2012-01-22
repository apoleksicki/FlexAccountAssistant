'''
Created on 31/10/2011

@author: Antek
'''

import unittest
from datetime import time
from flexaccountassistent.core.infrastructure.flexAccount import FlexAccount



class FlexAccountTest(unittest.TestCase):
    def testHourChangeMinus(self):
        expectedHours = 9
        expectedMinutes = 0
        flexAccount = FlexAccount(time(8, 20))
        flexAccount.sumTime(0, 40)
        print "Comparing hours"
        self.assertEquals(expectedHours, flexAccount.hours)
        print "Comparing minutes"
        self.assertEquals(expectedMinutes, flexAccount.minutes)
    
    def testHourChangePlus(self):
        self.makeTest(time(8, 20), 0, 50, 9, 10)
        
    def testNoHourChange(self):
        self.makeTest(time(8, 20), 0, -10, 8, 10)
    
    def testNegativeBalance(self):
        self.makeTest(time(8, 20), -9, -10, 0, -50)
    
    
    
    def makeTest(self, initialBalance, hoursToSum, minutesToSum, expectedHours, expectedMinutes):
        flexAccount = FlexAccount(initialBalance)
        flexAccount.sumTime(hoursToSum, minutesToSum)
        print "Comparing hours"
        self.assertEquals(expectedHours, flexAccount.hours)
        print "Comparing minutes"
        self.assertEquals(expectedMinutes, flexAccount.minutes)
    
        