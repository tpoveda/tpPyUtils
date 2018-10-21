#! /usr/bin/env python

"""
Module thata contains interfaces class for different purposes
"""


from __future__ import print_function, division, absolute_import, unicode_literals


class ISerializable(object):
    """
    Interface class used to identify serializable/deserializable classes
    """

    def __init__(self):
        super(ISerializable, self).__init__()

    def serialize(self, *args, **kwargs):
        """
        Serializes the current class
        """

        raise NotImplementedError('serialize method of ISerializable is not implemented!')

    def deserialize(self, *args, **kwargs):
        """
        Deserialize the current class
        """

        raise NotImplementedError('deseriailze method of ISerializable is not implemented!')