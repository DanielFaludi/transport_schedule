#!/usr/bin/python3

"""
This module contains a set of exceptions
"""

class InvalidInput(Exception):
    """
    Raised if invalid input was entered
    """

    def __init__(self, message):
        super().__init__(message)


class NotFound(Exception):
    """
    Raised if external API didn't find any results
    """

    def __init__(self, message):
        super().__init__(message)