#!/usr/bin/env python3

from TestSuiteTests import *
from TestCaseTests import *
from TestResultsTests import *
from ExpectTests import *
from ExpectNotTests import *
from ConsoleTestRunnerTests import *

if __name__ == "__main__":
    results = TestResults()
    suite = TestResultsTests.suite()
    suite.run(results)

    suite = TestCaseTests.suite()
    suite.run(results)

    suite = TestSuiteTests.suite()
    suite.run(results)

    suite = ExpectTests.suite()
    suite.run(results)

    suite = ExpectNotTests.suite()
    suite.run(results)

    suite = ConsoleTestRunnerTests.suite()
    suite.run(results)

    print(results.summary())
    exit(results.failCount > 0)
