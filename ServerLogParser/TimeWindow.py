
import datetime as dt

class TimeWindow():
    
    def __init__(self, start, end, parsedLog):
        self.start = start
        self.end = end
        
        self.parsedLog = parsedLog
        self.timestampStart = None
        self.timestampEnd = None
        
    def create_timeframe(self):
        now = dt.datetime.now()
        delta = dt.timedelta(minutes = - self.start)
        t = now.time()
        print("### Time: " + str(t))
        print("### Delta: " + str((dt.datetime.combine(dt.date(1,1,1),t) + delta).time()))
        newTime = str((dt.datetime.combine(dt.date(1,1,1),t) + delta).time())[0:8]
        self.timestampStart = newTime
        return newTime
        # Example 
        # awk '$0 > "12:55:10"' /var/log/jbossas/standalone/server.log > timeWindowTempLogFile
        # Oneliner for show only ERROR lines starting from timestamp:
        # grep ERROR /var/log/jbossas/standalone/server.log |  awk '$0 > "12:55:10"'
    
    def get_timeframe(self):
        times = ()
        times = (self.timestampStart, )