#!/usr/bin/env python3

# Copyright 2013 Iain Peddie inr314159@hotmail.com
# 
#    This file is part of WellBehavedPython
#
#    WellBehavedPython is free softwaree: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WellBehavedPython is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WellBehavedPython. If not, see <http://www.gnu.org/licenses/>.


import os
import os.path
import sys
from WellBehavedPython.TestCase import *
from WellBehavedPython.TestSuite import *

class TestSuiteTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    @staticmethod
    def suite():
        testMethods = [
            "test_running_suite_with_one_test_runs_one_test", 
            "test_running_suite_with_two_tests_runs_both"        ]
        suite = TestSuite()
    
        for testMethod in testMethods:
            suite.add(TestSuiteTests(testMethod))
        
        return suite

    def before(self):
        self.testMethodCount = 0
        self.suite = TestSuite()
        self.results = TestResults()

    def selfShuntIncrementMethod(self):
        self.testMethodCount += 1
        
    def test_running_suite_with_one_test_runs_one_test(self):
        test = TestSuiteTests("selfShuntIncrementMethod")
        self.suite.add(test)

        self.suite.run(self.results)
        assert(test.testMethodCount == 1)
        assert(self.results.summary() == "0 failed from 1 test")

    def test_running_suite_with_two_tests_runs_both(self):
        test1 = TestSuiteTests("selfShuntIncrementMethod")
        test2 = TestSuiteTests("selfShuntIncrementMethod")

        self.suite.add(test1)
        self.suite.add(test2)
        
        self.suite.run(self.results)

        assert(test1.testMethodCount == 1)
        assert(test2.testMethodCount == 1)
        assert(self.results.summary() == "0 failed from 2 tests")

if __name__ == "__main__":
    # Let's hand craft a test suite
    
    suite = TestSuiteTests.suite()
    
    results = TestResults()
    suite.run(results)
    
    print(results.summary())

