#!/usr/bin/env python3

class Expect:
    """Class used to indicate expected outcomes."""

    def __init__(self, condition):
        pass

    def fail(self):
        raise AssertionError()
