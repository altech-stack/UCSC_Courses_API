import logging
from logging.handlers import RotatingFileHandler

class LoggerHelpers():
    def __init__(self):
        # Writes all server and compute logs to a file, allows you to also rotate them
        handler = RotatingFileHandler('server_access.log', maxBytes=1000000, backupCount=2)
        self.logger = logging.getLogger('werkzeug')
        self.logger.addHandler(handler)
        self.logger = logging.getLogger('ucsc_courses')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)



    def log_msg(self,msg,severity=None):
        print (msg)
        if severity == "INFO":
            self.logger.info(msg)
        if severity == "DEBUG":
            self.logger.debug(msg)
        if severity == "ERROR":
            self.logger.error(msg)

        # There's a chance the developer could forget the severity levels.
        else:
            self.logger.info(msg)