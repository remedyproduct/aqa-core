from allure.allure import error_message
from helper.echo import echo, ECHO_COLORS


def event_wrapper(**kwargs):
    def inner(function):
        def wrapper(*args):
            data = _generate_data(args)
            result = function(*args)
            color = get_color(kwargs['method_name'], result)
            status = get_status(result)
            echo('[Data: %s] [Method: %s] [Status: %s]' % (data, kwargs['method_name'], status), color=color)
            _hard_assert_true(kwargs['method_name'], result, args)
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
        return 'empty'
    items = ''
    for item in args[0]:
        if item is not None:
            items += '%s; ' % str(item)
    return items[:-1]
