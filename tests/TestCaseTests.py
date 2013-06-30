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
        self.log += "before "

    def after(self):
        self.log += "after "

    def targetGoodMethod(self):
        """Target method when running unit tests."""
        self.log += "targetMethod "

    def targetErrorMethod(self):
        raise Exception

    def test_run_template_on_good_method(self):
        # we can't use self shunt here, because we need to
        # test for the after case. If we were self-shunting,
        # then after would be called after this test, which
        # would mean we couldn't test for it...
        test = TestCaseTests("targetGoodMethod")
        test.run()
        
        assert test.log == "before targetMethod after "

    def test_run_template_on_error_method(self):
        test = TestCaseTests("targetErrorMethod")
        test.run()

        assert test.log == "before after "
        
if __name__ == "__main__":
    TestCaseTests("test_run_template_on_good_method").run()
    TestCaseTests("test_run_template_on_error_method").run()

