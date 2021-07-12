from datetime import date
from datetime import datetime


class ECHO_COLORS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def echo(msg="-", color=None):
    if color:
        console_text = \
            '%s[%s::%s] %s %s' \
            % (color, date.today(), datetime.now().strftime("%H:%M:%S"), msg, ECHO_COLORS.ENDC)
    else:
        console_text = '[%s::%s] %s' % (date.today(), datetime.now().strftime("%H:%M:%S"), msg)
    print(console_text)
    return console_text
