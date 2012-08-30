#$Id: log.py,v 1.1 2007/12/07 06:02:16 test Exp $#
# -*- coding:gb2312 -*-

#################################################################
# Log class
# by ffb[hoker.ffb@gmail.com]
# last update: 2007-11-27
# homepage: http://mutong.saveasdf.com/
# project homepage: http://gforge.osdn.net.cn/projects/rpg2/
#################################################################
class Log:
    DebugLevel_Debug = 1;
    DebugLevel_Info	 = 2;
    DebugLevel_Warn	 = 3;
    DebugLevel_Error = 4;
    DebugLevel_Fatal = 5;
    
    # Current log level
    debugLevel = DebugLevel_Info;
    
    @staticmethod
    def debug(log):
        if(Log.debugLevel<=Log.DebugLevel_Debug):
            try:
                print('[DEBUG]' + log + '[/DEBUG]')
            except:
                print('[LOG ERROR/]')
    
    @staticmethod
    def info(log):
        if(Log.debugLevel<=Log.DebugLevel_Info):
            try:
                print('[INFO]' + log + '[/INFO]')
            except:
                print('[LOG ERROR/]')
    
    @staticmethod
    def warn(log):
        if(Log.debugLevel<=Log.DebugLevel_Warn):
            try:
                print('[WARN]' + log + '[/WARN]')
            except:
                print('[LOG ERROR/]')
  
    @staticmethod
    def error(log):
        if(Log.debugLevel<=Log.DebugLevel_Error):
            try:
                print('[ERROR]' + log + '[/ERROR]')
            except:
                print('[LOG ERROR/]')
    
    @staticmethod
    def fatal(log):
        if(Log.debugLevel<=Log.DebugLevel_Fatal):
            try:
                print('[FATAL]' + log + '[/FATAL]')
            except:
                print('[LOG ERROR/]')

    @staticmethod
    def getDebugLevel():
        return Log.debugLevel
    
    @staticmethod
    def setDebugLevel(debugLevel):
        Log.debugLevel = debugLevel;
  
def testCase():
    Log.setDebugLevel(Log.DebugLevel_Debug)
    Log.debug("debug")
    Log.info("info")
    Log.warn("warn")
    Log.error("error")
    Log.fatal("fatal")
    
if __name__ == '__main__':
    testCase()
