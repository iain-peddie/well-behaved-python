#!/usr/bin/env python3
from WellBehavedPythonTests.ConsoleTestRunnerTests import *
from WellBehavedPythonTests.ExpectNotTests import *
from WellBehavedPythonTests.ExpectTests import *
from WellBehavedPythonTests.TestCaseTests import *
from WellBehavedPythonTests.TestSuiteTests import *
from WellBehavedPythonTests.TestResultsTests import *
from WellBehavedPythonTests.TestResultTests import *
from WellBehavedPythonTests.VerboseConsoleTestRunnerTests import *


case = TestSuiteTests("test_error_in_afterClass_doesnt_mark_any_extra_errors")
case = TestSuiteTests("test_running_suite_with_two_tests_runs_both")
case = TestResultsTests("test_that_registering_tests_after_suites_delegate_to_suite_results")

case = TestSuiteTests("test_error_in_afterClass_doesnt_mark_any_extra_errors")
results = TestResults()
case.run(results)

print(results.summary())
