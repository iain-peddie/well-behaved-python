#!/usr/bin/env python3

import os
import os.path
import sys
from WellBehavedPython.TestCase import *

class TestCaseTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def before(self):
        self.wasBeforeCalled = True

    def targetMethod(self):
        """Target method when running unit tests."""
        self.wasTargetMethodCalled = True

    def test_run_template(self):
        self.targetMethod()
        
        assert self.wasBeforeCalled
        assert self.wasTargetMethodCalled        
        
if __name__ == "__main__":
    TestCaseTests("test_run_template").run()

