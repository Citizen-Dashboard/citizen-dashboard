import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys
from datetime import datetime




_log_level_string_to_level = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET
}


_logFormat = '%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d:%(funcName)s || %(message)s'
_log_directory = os.path.join(os.path.dirname(__file__), '..', 'logs')
_log_file_name = "data-aggregator"


class _File_Handler():
    """
    A class to handle file logging with a TimedRotatingFileHandler.

    This class sets up a file handler for logging that rotates logs daily and keeps
    backups for a specified number of days. It uses the logging level specified in
    the environment variables.

    Attributes:
        level (int): The logging level, obtained from environment variables.
        file_handler (TimedRotatingFileHandler): The configured file handler for logging.

    Methods:
        __init__(): Initializes the _File_Handler with the appropriate logging setup.
        get_file_handler(): Returns the configured file handler.
    """
    def __init__(self):
         # determine log path and date stamped file name. Create directory if it doesn't exist
        today = datetime.now().strftime('%Y-%m-%d')   
        log_path = os.path.join(_log_directory, f'{str(_log_file_name).replace(" ", "_")}_{today}.log')
        
        # create log directory if it doesn't exist
        try:
            os.makedirs(_log_directory, exist_ok=True)
        except Exception as e:
            print(f"Error creating log directory: {e}")
            return
        
        self.file_handler = TimedRotatingFileHandler(log_path, when='D', interval=1, backupCount=3, encoding='utf-8')
        self.file_handler.setLevel(os.environ.get('log_level'))
        self.file_handler.setFormatter(logging.Formatter(_logFormat))        
        print(f"******** File Logger initialized with loglevel: {os.environ.get('log_level')}. Log file: {log_path}")
        
    def get_file_handler(self):
        return self.file_handler


_rotating_file_handler = _File_Handler().get_file_handler()



class File_Console_Logger(logging.getLoggerClass()):
    """
    A custom logger class that supports both file and console logging.

    This class extends the base logging.Logger class to provide a convenient way
    to set up logging to both a file and the console. It uses a rotating file
    handler for file logging and a stream handler for console logging.

    Attributes:
        name (str): The name of the logger.
        level (int): The logging level, obtained from environment variables.
        std_out_handler (logging.StreamHandler): Handler for console logging.

    Methods:
        __init__(name, enable_console_logging=True, enable_file_logging=True):
            Initializes the logger with the specified name and logging options.
    """
    
    def __init__(self, name, enable_console_logging:bool=True, enable_file_logging:bool=True):
        super().__init__(name)
        self.setLevel(os.environ.get('log_level'))
        
        if enable_console_logging:
            # setup standard out logging
            self.std_out_handler = logging.StreamHandler(sys.stdout)
            self.std_out_handler.setLevel(self.level)
            self.std_out_handler.setFormatter(logging.Formatter(_logFormat))
            self.addHandler(self.std_out_handler)
            print("console logging enabled.")


        if enable_file_logging:
            # setup file logging
            self.addHandler(_rotating_file_handler)
            print("File logging enabled.")

