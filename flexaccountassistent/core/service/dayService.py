'''
Created on 22/01/2012

@author: Antek
'''

import datetime
import os
from datetime import time
from string import atoi
from flexaccountassistent.core.infrastructure.day import Day

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
    separator = DayRepositoryTextFile._separator
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
    toReturn += '\n'
    
   
    return toReturn

def createFileContent():
    pass
    
        
def parserDayLine(line):
    splited = line.split(DayRepositoryTextFile._separator)
    splittedDate = splited[Day.DATE].split('-')
    year = int(splittedDate[0])
    month = int(splittedDate[1])
    day = int(splittedDate[2])
    
    date = datetime.date(year, month, day)
    pause = int(splited[Day.PAUSE])
    startTime = _parseTime(splited[Day.START_TIME])
    endTime = _parseTime(splited[Day.END_TIME])
    
    toReturn = Day(date, pause, startTime)
    toReturn.setStop(endTime)
    
    return toReturn

def _parseTime(timeToParse):
    splited = timeToParse.split(':')
    hour = int(splited[0])
    minute = int(splited[1])
    
    return time(hour, minute)
    
    


class DayRepositoryTextFile (DayRepository):
    u"""Implementation of DayRepository, that bases on a flat text file""" 
    _path = 'faa.txt'
    _separator = ";"
    
    def __init__(self, initialBalanceInMinutes=0, path = None):
        DayRepository.__init__(self)
        self.__days = {}
        self.initialBalance = initialBalanceInMinutes
        self.balance = 0
        if initialBalanceInMinutes == 0:
            try:
                if path == None:
                    path = DayRepositoryTextFile._path
                repoFile = open(path, 'r')
                self._readFileContent(repoFile)
                repoFile.close();
            except IOError:
                print 'Could not found the save file'
        else:
            print 'Starting repository without save file'
            
        #if file.
        #catch:
        #pass
            
    def _readFileContent(self, repoFile):
        line = repoFile.readline()
        self.initialBalance =  atoi(line)
        line = repoFile.readline()
        while line != None and line !='':
            self.addDay(parserDayLine(line))
            line = repoFile.readline()
       
        
        
        
    
    def addDay(self, day):
        if self.__days.get(day.date) != None:
            self.balance -= self.__days.pop(day.date).countTime() - day.workingMinutes
            
        self.__days[day.date] = day
        self.balance += day.countTime() - day.workingMinutes
    
    def getBalance(self):
        return self.balance + self.initialBalance
    
    def __createContent(self):
        toReturn = []
        toReturn.append(self.initialBalance)
        toReturn.append([dayParser(value) for value in self.__days.values()])
        return toReturn
    
    def __export(self):
        balancePossition = 0
        daysPossition = 1
        try:
            os.remove(DayRepositoryTextFile._path)
        except:
            print "File does not exist"
        f = open(DayRepositoryTextFile._path, 'wb')
        print 'File opened'
        content = self.__createContent()
        f.write("%i\n" % content[balancePossition]);
        f.writelines(content[daysPossition])
        f.close()
        print 'File closed'
        return content
        
        
    def close(self):
        return self.__export()
    
