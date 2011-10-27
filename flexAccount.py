'''
Created on 27/10/2011

@author: Antek
'''

from datetime import time

class FlexAccount(object):
    """Hold balane of the flex account"""
    
    def __init__(self, initialState = None):
        object.__init__(self)
        
        if initialState == None:
            self.hours = 0
            self.minutes = 0
        else:
            self.hours = initialState.hour
            self.minutes = initialState.minute
        
    
    def sumTime(self, timeToSum):
        self.hours = self.hours - timeToSum.hour
        self.minutes = self.minutes - timeToSum.minute
        
        if self.minutes < 0:
            self.hours = self.hours - 1
            self.minutes = self.minutes + 60
            
        
        