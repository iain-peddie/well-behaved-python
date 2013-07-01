#!/usr/bin/env python3

class Expect:
    """Class used to indicate expected outcomes."""

    def __init__(self, actual):
        self.actual = actual

    def fail(self, Message = ""):
        raise AssertionError(Message)

    def toEqual(self, expected):
        if self.actual == expected:
            pass
        else:
            self.fail("Expected {} but actual value is {}".format(expected, self.actual))
