'''
Created on 24/10/2011

@author: Antek
'''

import datetime
#from datetime import time
#from datetime import datetime

class Day(object):
    '''
    classdocs
    '''


    def __init__(self, date = date.today(), pause=30, start_time = time(8, 20)):
        '''
        Constructor
        '''
        self.date = date
        self.pause = pause
        self.start_time = start_time
        working_hours = 0
        end_time = None
        
    def set_stop(self, end_time = datetime.datetime.now()):
        self.end_time = end_time
        
    def count_time(self):
        hours = self.end_time.hour - self.start_time.hour
        minutes = self.end_time.minute - self.start_time.minute
        return time(hours, minutes)
        
    
        