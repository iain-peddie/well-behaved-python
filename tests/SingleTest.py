#!/usr/bin/env python3

from WellBehavedPythonTests.Discovery.TestDiscovererTests import *
from WellBehavedPython.Runners.VerboseConsoleTestRunner import *

case = TestDiscovererTests()
case.configureTest("test_can_filter_out_modules")

runner = VerboseConsoleTestRunner()
runner.run(case)

print(results.summary())
