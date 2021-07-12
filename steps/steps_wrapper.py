import math
import time
from helper.echo import echo, ECHO_COLORS


def step_wrapper(**kwargs):
    def inner(function):
        def wrapper(*args, **fwargs):
            echo('[Step name: %s]' % (kwargs['step_name']), color=ECHO_COLORS.HEADER)
            start_time = time.time()
            result = function(*args, **fwargs)
            echo('[Step time: %s seconds]' % (math.ceil(time.time() - start_time)), color=ECHO_COLORS.OKBLUE)
            return result
        return wrapper
    return inner
