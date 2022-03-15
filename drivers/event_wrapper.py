import math
import time
from allure.allure import error_message
from helper.echo import echo, ECHO_COLORS
from locators.locator import Locator

NOT_IGNORE = [
    'Open Application', 'Close Application', 'Reopen Application', 'Reset Application',
    'Displayed', 'Not Displayed',
    'Click', 'Clear', 'Input', 'Clean Input', 'Text',
    'Dropdown Select', 'URL', 'Set Image', 'Refresh Page',
    'Tap', 'Take Photo'
]


def event_wrapper(**kwargs):
    def inner(function):
        def wrapper(*args):
            start(kwargs['method_name'], *args)
            start_time = time.time()
            result = function(*args)
            end(kwargs['method_name'], start_time)
            return result
        return wrapper
    return inner


def get_status(result: bool):
    return 'Passed' if result else 'Fail'


def get_color(method_name: str, result: bool):
    if result:
        if method_name == 'wait':
            return ECHO_COLORS.WARNING
        return ECHO_COLORS.OKGREEN
    else:
        return ECHO_COLORS.FAIL


def _hard_assert_true(method_name: str, result: bool, args):
    if method_name in ['exists', 'not exists'] and result is False:
        msg = '[Method: %s] [Element: %s] [Status: Fail]' % (method_name, args[1].description)
        echo(msg, color=ECHO_COLORS.FAIL)
        error_message(msg, args[0])
        assert result, msg


def _generate_data(*args):
    if len(args) == 0:
        return 'Empty'
    items = ''
    for item in args[0]:
        if item is not None:
            items += '%s; ' % str(item)
    return items[:-1]


def start(method_name, *args):
    if method_name in NOT_IGNORE:
        echo('The %s method has been started.' % method_name, ECHO_COLORS.BOLD)
        if method_name in ['Open Application', 'Close Application', 'Reopen Application', 'Reset Application']:
            echo('Platform: %s' % args[0], ECHO_COLORS.ENDC)
        if method_name in ['Displayed', 'Not Displayed', 'Click', 'Clear']:
            locator = args[1]
            dynamic_value = 'without'
            if len(args) > 2:
                dynamic_value = 'with "%s"' % args[2]
            echo('Locator: %s %s dynamic value.' % (locator.description, dynamic_value), ECHO_COLORS.ENDC)
        if method_name in ['Input', 'Clean Input']:
            locator = args[1]
            dynamic_value = 'without'
            if len(args) > 4:
                dynamic_value = 'with "%s"' % args[4]
            echo(
                'Locator: %s %s dynamic value. Input text is "%s".'
                % (locator.description, dynamic_value, args[2]),
                ECHO_COLORS.ENDC
            )


def end(method_name, start_time):
    if method_name in NOT_IGNORE:
        end_time = math.ceil(time.time() - start_time)
        echo(
            'The %s method was over. Its time is %s seconds.' % (method_name, end_time),
            ECHO_COLORS.UNDERLINE
        )
        if end_time > 50 \
                and method_name in ['Displayed', 'Not Displayed', 'Click', 'Clear', 'Input', 'Clean Input', 'Text']:
            echo('Very long execution time, namely %s seconds.' % end_time, ECHO_COLORS.FAIL)
