#encoding:utf-8
import logging

#get defaults from settings
#if not found set defaults 
#from hardcoded values
try :
    from django.conf import settings
    
    default_format = getattr(settings, 'LOG_FORMAT')
    default_date_format = getattr(settings, 'LOG_DATE_FORMAT')
    default_level_file = getattr(logging, settings.LOG_LEVEL_FILE)
    default_level_console = getattr(logging, settings.LOG_LEVEL_CONSOLE)
except :
    default_format = '%(asctime)s, %(name)s [%(levelname)s] : %(message)s'
    default_date_format = "%Y/%m/%d %H:%M:%S"
    default_level_file = logging.DEBUG
    default_level_console = logging.INFO

logging.HEADER = 60
logging.addLevelName(logging.HEADER, 'HEADER')

def logger_header(self, msg, *args, **kwargs):
    if self.manager.disable >= logging.HEADER:
        return
    if logging.HEADER >= self.getEffectiveLevel():
        apply(self._log, (logging.HEADER, msg, args), kwargs)
        
logging.Logger.header = logger_header
    
def create_console_handler():
    """Create a console handler."""
    handler = logging.StreamHandler()
    handler.setLevel(default_level_console)
    handler.setFormatter(logging.Formatter(default_format, default_date_format))
    return handler

def create_console(name):
    """Console based logging facility."""
    console_handler = create_console_handler()
    console = logging.getLogger(name)
    console.addHandler(console_handler)
    return console

def create_file_handler(location, mode):
    """Create an handler for the specified file location."""
    handler = logging.FileHandler(location, mode)
    handler.setLevel(default_level_file)
    handler.setFormatter(logging.Formatter(default_format, default_date_format))
    return handler

def create_logger(name, mode):
    """File based logging facility."""
    location = settings.LOGS_LOCATION + '/%s.log' % (name)
    file_handler = create_file_handler(location, mode)
    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    return logger

def create_mixed_logger(name, mode):
    """File and console based logging facility."""
    location = settings.LOGS_LOCATION + '/%s.log' % (name)
    console_handler = create_console_handler()
    file_handler = create_file_handler(location, mode)
    mixed_logger = logging.getLogger(name)
    mixed_logger.addHandler(console_handler)
    mixed_logger.addHandler(file_handler)
    return mixed_logger

def default_logger(name) :
    """
    Create a mixed logger if settings.DEBUG 
    is set to True else create a console one.
    """
    return create_mixed_logger(name, 'a') if settings.DEBUG else create_console(name)
        
