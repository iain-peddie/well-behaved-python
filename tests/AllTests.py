#!/usr/bin/env python3

from TestSuiteTests import *
from TestCaseTests import *
from TestResultsTests import *
from ExpectTests import *
from ExpectNotTests import *
from ConsoleTestRunnerTests import *

from WellBehavedPython.TestSuite import TestSuite
from WellBehavedPython.ConsoleTestRunner import ConsoleTestRunner

if __name__ == "__main__":
    results = TestResults()
    runner = ConsoleTestRunner()
    suite = TestSuite()
    suite.add(TestResultsTests.suite())
    suite.add(TestCaseTests.suite())
    suite.add(TestSuiteTests.suite())
    suite.add(ExpectTests.suite())
    suite.add(ExpectNotTests.suite())
    suite.add(ConsoleTestRunnerTests.suite())
    results = runner.run(suite)

    exit(results.failCount > 0)
