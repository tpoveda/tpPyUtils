#! /usr/bin/env python

"""
Module that contains utility functions related with debugging purposes
"""


from __future__ import print_function, division, absolute_import, unicode_literals


# region Functions
def format_message(fname, expected, actual, flag):
    """
    Convenience function that returns nicely formatted error/warning messages
    """

    format = lambda types: ', '.join([str(t).split("'")[1] for t in types])
    expected, actual = format(expected), format(actual)
    msg = "'{}' method ".format(fname) + ('accepts', 'returns')[flag] + ' ({}), but '.format(expected) + \
          ('was given', 'result is')[flag] + ' ({})'.format(actual)
    return msg


def debug_object_string(obj, msg):
    """
    Returns a debug string depending of the type of the object
    :param obj: Python object
    :param msg: message to log
    :return: str, debug string
    """

    import inspect
    # debug a module
    if inspect.ismodule(obj):
        return '[%s module] :: %s' % (obj.__name__, msg)

    # debug a class
    elif inspect.isclass(obj):
        return '[%s.%s class] :: %s' % (obj.__module__, obj.__name__, msg)

    # debug an instance method
    elif inspect.ismethod(obj):
        return '[%s.%s.%s method] :: %s' % (obj.im_class.__module__, obj.im_class.__name__, obj.__name__, msg)

    # debug a function
    elif inspect.isfunction(obj):
        return '[%s.%s function] :: %s' % (obj.__module__, obj.__name__, msg)
# endregion