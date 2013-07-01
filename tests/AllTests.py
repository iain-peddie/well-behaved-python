#!/usr/bin/env python3

from TestSuiteTests import *
from TestCaseTests import *
from TestResultsTests import *
from ExpectTests import *

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

    print(results.summary())
