#!/usr/bin/env python3

from WellBehavedPython.it import it
from WellBehavedPython.TestCommand import *


class WasRun:

    def __init__(self, testFunctionName):
        pass

    def run(self):
        self.test_TestCommand_runsTest()

    def targetMethod(self):
        """Target method when running unit tests."""
        self.wasRun = True

    def test_TestCommand_runsTest(self):
        tester = self
        test = TestCommand(tester.targetMethod)
        test.run()
        assert tester.wasRun
        

