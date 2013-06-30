#!/usr/bin/env python3

import os
import os.path
import sys
from WellBehavedPython.TestCase import *

class TestCaseTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)
        self.log = ""

    def before(self):
        self.wasBeforeCalled = True
        self.log += "before "

    def targetMethod(self):
        """Target method when running unit tests."""
        self.wasTargetMethodCalled = True
        self.log += "targetMethod "

    def test_run_template(self):
        # we can't use self shunt here, because we need to
        # test for the after case. If we were self-shunting,
        # then after would be called after this test, which
        # would mean we couldn't test for it...
        test = TestCaseTests("targetMethod")
        test.run()
        
        assert test.log == "before targetMethod "
        
if __name__ == "__main__":
    TestCaseTests("test_run_template").run()

