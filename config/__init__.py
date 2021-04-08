'''
oskar.eiriksson@contentstack.com
2020-09-28

Some config functions
'''
import logging

logLevel = logging.INFO # Possible levels e.g.: DEBUG, ERROR, INFO
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logLevel)

# Text formatting for terminal logs.
PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
WHITE = '\033[0;37m'
REDBG = '\033[0;41m'
GREENBG = '\033[0;42m'
END = '\033[0m'
