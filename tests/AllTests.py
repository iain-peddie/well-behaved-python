#!/usr/bin/env python3

import sys



from WellBehavedPythonTests.ConsoleTestRunnerTests import *
from WellBehavedPythonTests.ExpectNotTests import *
from WellBehavedPythonTests.ExpectTests import *
from WellBehavedPythonTests.TestCaseTests import *
from WellBehavedPythonTests.TestSuiteTests import *
from WellBehavedPythonTests.TestResultsTests import *
from WellBehavedPythonTests.TestResultTests import *
from WellBehavedPythonTests.VerboseConsoleTestRunnerTests import *

from WellBehavedPython.TestSuite import TestSuite
from WellBehavedPython.ConsoleTestRunner import ConsoleTestRunner

if __name__ == "__main__":
    try:
        results = TestResults()
        runner = ConsoleTestRunner(bufferOutput = True)
        suite = TestSuite()
        suite.add(TestResultTests.suite())
        suite.add(TestResultsTests.suite())
        suite.add(TestCaseTests.suite())
        suite.add(TestSuiteTests.suite())
        suite.add(ExpectTests.suite())
        suite.add(ExpectNotTests.suite())
        suite.add(ConsoleTestRunnerTests.suite())
        suite.add(VerboseConsoleTestRunnerTests.suite())
        results = runner.run(suite)

        runner = VerboseConsoleTestRunner(bufferOutput = True)
        results = runner.run(suite)

        exit(results.failCount > 0)
    except Exception as ex:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        traceback.print_exc(file = sys.stdout)
        
    
