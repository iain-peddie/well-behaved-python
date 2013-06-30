#!/usr/bin/env python3

from WellBehavedPython.TestCase import *
from WellBehavedPython.TestResults import *

class TestResultsTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def test_summary_for_single_passing_test(self):
        results = TestResults()
        results.registerTestStarted()

        assert results.summary() == "0 failed from 1 test"

    def test_summary_for_two_passing_tests(self):
        results = TestResults()
        results.registerTestStarted()
        results.registerTestStarted()

        assert results.summary() == "0 failed from 2 tests"

if __name__ == "__main__":
    # Let's hand craft a test suite

    testMethods = [
        "test_summary_for_single_passing_test",
        "test_summary_for_two_passing_tests"
        ]

    for testMethod in testMethods:
        print("running {}".format(testMethod))
        results = TestResultsTests(testMethod).run()
        print(results.summary())

