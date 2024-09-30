import logging
from logging import Logger
from enum import Enum
from datetime import datetime

class Logtype(Enum):
    CONNECTION = "Connection"
    RECIEVED   = "Recieved"
    RESET      = "Reset"
    BOOT       = "Boot"
    ERROR      = "Error"


class Logger:
    def __init__(self, log_file="logger.log", log_level=logging.INFO, log_types=None):
         
