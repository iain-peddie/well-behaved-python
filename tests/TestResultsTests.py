#!/usr/bin/env python3

from WellBehavedPython.TestCase import *
from WellBehavedPython.TestResults import *

class TestResultsTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def before(self):
        self.results = TestResults()
        self.results.registerTestStarted()

    def test_summary_for_single_passing_test(self):
        results = self.results

        assert results.summary() == "0 failed from 1 test"

    def test_summary_for_two_passing_tests(self):
        results = self.results
        results.registerTestStarted()

        assert results.summary() == "0 failed from 2 tests"

    def test_summary_for_single_failing_test(self):
        results = self.results
        results.registerTestFailed()

        assert results.summary() == "1 failed from 1 test"

    def test_summary_for_passing_and_failing_test(self):
        results = self.results
        results.registerTestFailed()
        results.registerTestStarted()

        assert results.summary() == "1 failed from 2 tests"
        

if __name__ == "__main__":
    # Let's hand craft a test suite

    testMethods = [
        "test_summary_for_single_passing_test",
        "test_summary_for_two_passing_tests",
        "test_summary_for_single_failing_test",
        "test_summary_for_passing_and_failing_test",
        ]

    for testMethod in testMethods:
        results = TestResultsTests(testMethod).run()
        print(results.summary())

