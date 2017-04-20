from __future__ import unicode_literals
import sys
import functools


PY3 = sys.version_info[0] == 3


def validate_string(s):
    """
    Check input has length and that length > 0

    :param s:
    :return: True if len(s) > 0 else False
    """
    try:
        return len(s) > 0
    except TypeError:
        return False


def check_for_none(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if args[0] is None or args[1] is None:
            return 0
        return func(*args, **kwargs)
    return decorator


def check_empty_string(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if len(args[0]) == 0 or len(args[1]) == 0:
            return 0
        return func(*args, **kwargs)
    return decorator


def make_type_consistent(s1, s2):
    """If both objects aren't either both string or unicode instances force them to unicode"""
    if isinstance(s1, str) and isinstance(s2, str):
        return s1, s2

    elif isinstance(s1, unicode) and isinstance(s2, unicode):
        return s1, s2

    else:
        return unicode(s1), unicode(s2)


def intr(n):
    '''Returns a correctly rounded integer'''
    return int(round(n))
