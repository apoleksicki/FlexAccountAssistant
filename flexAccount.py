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
        
    
    def sumTime(self, hours, minutes):
        
        if hours * minutes < 0:
            raise Exception
        
        balanceMinutes = self.hours * 60 + self.minutes
        minutesToAdd = hours * 60 + minutes
        balanceMinutes = balanceMinutes + minutesToAdd
        
        factor = 1
        if balanceMinutes < 0:
            factor = - 1
        self.hours = balanceMinutes * factor / 60
        self.minutes = balanceMinutes * factor % 60
        self.hours *= factor
        self.minutes *= factor
#        self.minutes = self.minutes + minutes
#        
#        if self.hours 
#        if self.minutes < 0:
#            self.hours = self.hours - 1
#            self.minutes = self.minutes + 60
#        if self.minutes > 59:
#            self.hours = self.hours + 1
#            self.minutes = self.minutes - 60
            
        
        