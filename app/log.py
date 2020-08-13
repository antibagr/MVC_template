import sys
import logging
import os
import time
from logging.handlers import RotatingFileHandler

from app.settings import DEBUG,MAXLOGCOUNT

def setupLogger():

    def consoleLogger(logger):
        consoleLog = logging.StreamHandler()
        consoleLog.setLevel(level)
        logConsoleFormat = logging.Formatter()
        consoleLog.setFormatter(logConsoleFormat)
        logger.addHandler(consoleLog)

    def fileLogger(logger,fileLogLevel=None):

        global MAXLOGCOUNT

        if MAXLOGCOUNT == 0:
            return

        MAXLOGCOUNT = MAXLOGCOUNT if MAXLOGCOUNT > 1 else 1

        fileLogLevel = fileLogLevel if fileLogLevel else logging.DEBUG

        if not os.path.exists('logs'):
            os.mkdir('logs')

        logFileName = 'prebuild-' + time.strftime("%Y%m%d-%H%M%S")

        logList = os.listdir('logs')
        logList.sort()
        if len(logList) > MAXLOGCOUNT-1:
            try:
                os.remove(os.path.join('logs',logList[0]))
            except FileNotFoundError:
                logger.critical("Exception while removing old logs")

        logFilePath = os.path.join('logs',logFileName + '.log')

        fileLog = RotatingFileHandler(logFilePath, mode='w', maxBytes=50*1024*1024,
                                         backupCount=5, encoding=None, delay=False)

        fileLog.setLevel(fileLogLevel)
        logFileFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileLog.setFormatter(logFileFormat)
        logger.addHandler(fileLog)

    def handle_unhandled_exception(exc_type, exc_value, exc_traceback,thread_identifier=None):
        """Handler for unhandled exceptions that will write to the logs"""
        if issubclass(exc_type, KeyboardInterrupt):
            # call the default excepthook saved at __excepthook__
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        if thread_identifier:
            logger.critical(f"Unhandled exception in {thread_identifier}",exc_info=(exc_type, exc_value, exc_traceback))
        else:
            logger.critical(f"Unhandled exception",exc_info=(exc_type, exc_value, exc_traceback))

    level = logging.DEBUG if DEBUG else logging.ERROR
    logger = logging.getLogger("__main__")
    logger.setLevel(level)
    consoleLogger(logger)
    fileLogger(logger)
    sys.excepthook = handle_unhandled_exception
    return logger

logger = setupLogger()
