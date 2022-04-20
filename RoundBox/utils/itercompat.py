#  -*- coding: utf-8 -*-


def is_iterable(x):
    """An implementation independent way of checking for iterables
    :param x:
    :return:
    """
    try:
        iter(x)
    except TypeError:
        return False
    else:
        return True
