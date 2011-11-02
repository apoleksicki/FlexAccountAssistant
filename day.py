u'''
Created on 24/10/2011

@author: Antek
'''

import datetime
from time import mktime
from datetime import time
#from datetime import datetime

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
    classdocs
    '''


    def __init__(self, date=None, pause=30, startTime=None ):
        '''
        Constructor
        '''
        object.__init__(self)
        if date == None:
            self.date = datetime.date.today()
        if startTime == None:
            self.startTime = time(8, 20)
        else:
            self.startTime = startTime
        self.pause = pause
        working_hours = 0
        endEime = None
        
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
        
class DayService(object):
    u"""Class that provides basic interface for operations on the Day objects""" 
    
    def getTimeOnDay(self, day):
        pass
    
    def getBalance(self):  
        pass
    def addDay(self, day):
        pass  
    
class DictionaryDayService(DayService):
    u"""Basic implementation of DayService. Works on a dictionary"""
    def __init__(self, initialBalance=0):
        DayService.__init__(self)
        self.__days = {}
        self.initialBalance= initialBalance
        self.balance = 0
        
    def addDay(self, day):
        if self.__days.get(day.date) != None:
            self.balance -= self.__days[day.date].countTime()
        self.balance +=day.countTime()
    
    def getBalance(self):
        sumBalance = self.initialBalance
        for v in self.__days.values():
            sumBalance += v.countTime()
        return self.initialBalance
        
        
        
        
class DayRepository(object):
    u"""Interface for day repository"""
    def getTimeOnDay(self, day):
        pass
    
    def getBalance(self):  
        pass
    def addDay(self, day):
        pass  
    
    
    
        
        
        
     
        