u'''
Created on 24/10/2011

@author: Antek
'''

import datetime
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
    Class that represents a working day.
    '''
    NORMAL = 0
    HOLIDAY = 1 
    MINUTES_IN_HOUR = 60
    NORMAL_HOURS = 7.5
    FRIDAY_HOURS = 7

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
    def __init__(self, initialBalanceInMinutes=0, repository = None):
        DayService.__init__(self)
        
        self.__dayRepository = repository 
        if self.__dayRepository == None:
            self.__dayRepository =   DayRepositoryTextFile(initialBalanceInMinutes)
        
        
        
    def addDay(self, day):
        self.__dayRepository.addDay(day)
    
    def getBalance(self):
        return self.__dayRepository.getBalance()
    def close(self):
        self.__dayRepository.close()
        
        
        
        
class DayRepository(object):
    u"""Interface for day repository"""
    def getTimeOnDay(self, day):
        pass
    
    def getBalance(self):  
        pass
    def addDay(self, day):
        pass
    def close(self):
        pass  
    def export(self):
        pass
    

def dayParser(day):
    u"""Parses a day object into comma separated line, which can be used later to recreate object"""
    separator = ";"
    toReturn = ""
    toReturn += day.date.isoformat()
    toReturn += separator
    toReturn += "%d" % (day.pause)
    toReturn += separator
    toReturn += day.startTime.isoformat()
    toReturn += separator
    toReturn += "%d" % day._dayType
    toReturn += separator
    toReturn += day.endTime.isoformat()
    toReturn + "\n"
    
    
    return toReturn

def createFileContent():
    pass
    
        
class DayRepositoryTextFile (DayRepository):
    u"""Implementation of DayRepository, that bases on a flat text file""" 
    
    def __init__(self, initialBalanceInMinutes=0, path = None):
        DayRepository.__init__(self)
        self.__days = {}
        self.balance = initialBalanceInMinutes
        
    
    def addDay(self, day):
        if self.__days.get(day.date) != None:
            self.balance -= self.__days.pop(day.date).countTime() - day.workingMinutes
            
        self.__days[day.date] = day
        self.balance += day.countTime() - day.workingMinutes
    
    def getBalance(self):
        return self.balance
    
    def __createContent(self):
        return [dayParser(value) for value in self.__days.values()]
    
    def __export(self):
        content = self.__createContent()
        return content
        
        
    def close(self):
        return self.__export()
    
        
        
        
     
        