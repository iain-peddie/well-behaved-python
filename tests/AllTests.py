#!/usr/bin/env python3

import sys

from WellBehavedPythonTests.ConsoleTestRunnerTests import *
from WellBehavedPythonTests.ExpectNotTests import *
from WellBehavedPythonTests.ExpectTests import *
from WellBehavedPythonTests.TestCaseTests import *
from WellBehavedPythonTests.TestSuiteTests import *
from WellBehavedPythonTests.TestResultsTests import *
from WellBehavedPythonTests.VerboseConsoleTestRunnerTests import *

from WellBehavedPython.TestSuite import TestSuite
from WellBehavedPython.ConsoleTestRunner import ConsoleTestRunner

if __name__ == "__main__":
    try:
        results = TestResults()
        suite = TestSuite("AllTests")
        suite.add(TestResultsTests.suite())
        suite.add(TestCaseTests.suite())
        suite.add(TestSuiteTests.suite())
        suite.add(ExpectTests.suite())
        suite.add(ExpectNotTests.suite())
        suite.add(ConsoleTestRunnerTests.suite())
        suite.add(VerboseConsoleTestRunnerTests.suite())

        if len(sys.argv) > 1 and sys.argv[1] == '--verbose':
            runner = VerboseConsoleTestRunner(bufferOutput = True)
        else:
            runner = ConsoleTestRunner(bufferOutput = True)
        results = runner.run(suite)

        # TODO : is test run success
        exit(results.countFailures() + results.countErrors() > 0)
    except Exception as ex:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        traceback.print_exc(file = sys.stdout)
        
    
