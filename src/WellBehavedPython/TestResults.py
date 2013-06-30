#!/usr/bin/env python3

class TestResults:

    def __init__(self):
        self.testCount = 0
        self.failCount = 0

    def registerTestStarted(self):
        self.testCount += 1
    
    def summary(self):
        return "{} failed from {} test".format(
            self.failCount, self.testCount)
