#!/usr/bin/env python3

# Copyright 2013-4 Iain Peddie inr314159@hotmail.com
# 
#    This file is part of WellBehavedPython
#
#    WellBehavedPython is free software: you can redistribute it and/or modify
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

import sys

from WellBehavedPythonTests.Discovery.ModuleExaminerTests import *

from WellBehavedPythonTests.Engine.TestCaseTests import *
from WellBehavedPythonTests.Engine.TestSuiteTests import *
from WellBehavedPythonTests.Engine.TestResultsTests import *
from WellBehavedPythonTests.Engine.TestContextTests import *

from WellBehavedPythonTests.Expectations.StringExpectationsTests import *
from WellBehavedPythonTests.Expectations.DefaultExpectationsTests import *
from WellBehavedPythonTests.Expectations.ContainerExpectationsTests import *
from WellBehavedPythonTests.Expectations.DictionaryExpectationsTests import *
from WellBehavedPythonTests.Expectations.NumericExpectationsTests import *
from WellBehavedPythonTests.Expectations.MethodSpyExpectationsTests import *

from WellBehavedPythonTests.Fakes.MethodSpyTests import *
from WellBehavedPythonTests.Fakes.ObjectSpyTests import *
from WellBehavedPythonTests.Fakes.SpyOnTests import *

from WellBehavedPythonTests.ExpectationsRegistryTests import *
from WellBehavedPythonTests.BackwardsCompatibilityTests import *

from WellBehavedPythonTests.VerboseConsoleTestRunnerTests import *
from WellBehavedPythonTests.ConsoleTestRunnerTests import *


from WellBehavedPython.Engine.TestSuite import TestSuite
from WellBehavedPython.Runners.ConsoleTestRunner import ConsoleTestRunner


def main(suite):
    try:
        suite = createSuite()
        
        buffer = True

        if len(sys.argv) > 1 and sys.argv[1] == '--verbose':
            runner = VerboseConsoleTestRunner(bufferOutput = buffer)
        else:
            runner = ConsoleTestRunner(bufferOutput = buffer)
        results = runner.run(suite)

        sys.__stdout__.flush()
        sys.__stderr__.flush()

        exit(results.countFailures() + results.countErrors() > 0)
    except Exception as ex:        
    
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        traceback.print_exc(file = sys.stdout)
        
    
def createSuite():
    suite = TestSuite("WellBehavedPythonTests")
    engineSuite = TestSuite("Engine")
    expectationsSuite = TestSuite("Expectations")
    fakesSuite = TestSuite("Fakes")
    discoverySuite = TestSuite("Discovery")

    discoverySuite.add(ModuleExaminerTests.suite())

    engineSuite.add(TestResultsTests.suite())
    engineSuite.add(TestCaseTests.suite())
    engineSuite.add(TestSuiteTests.suite())
    engineSuite.add(TestContextTests.suite())

    expectationsSuite.add(DefaultExpectationsTests.suite())
    expectationsSuite.add(DefaultNotExpectationsTests.suite())
    expectationsSuite.add(NumericExpectationsTests.suite())
    expectationsSuite.add(NumericNotExpectationsTests.suite())
    expectationsSuite.add(StringExpectationsTests.suite())
    expectationsSuite.add(StringNotExpectationsTests.suite())
    expectationsSuite.add(ContainerExpectationsTests.suite())
    expectationsSuite.add(ContainerNotExpectationsTests.suite())
    expectationsSuite.add(DictionaryExpectationsTests.suite())
    expectationsSuite.add(DictionaryNotExpectationsTests.suite())
    expectationsSuite.add(MethodSpyExpectationsTests.suite())
    
    fakesSuite.add(MethodSpyNotExpectationsTests.suite())
    fakesSuite.add(MethodSpyTests.suite())
    fakesSuite.add(ObjectSpyTests.suite())
    fakesSuite.add(SpyOnTests.suite())
    
    
    suite.add(ConsoleTestRunnerTests.suite())
    suite.add(VerboseConsoleTestRunnerTests.suite())
    suite.add(ExpectationsFactoryTests.suite())
    suite.add(ExpectationsRegistryTests.suite())
    suite.add(BackwardsCompatibilityTests.suite())

    suite.add(engineSuite)
    suite.add(expectationsSuite)
    suite.add(fakesSuite)
    suite.add(discoverySuite)
    
    
    return suite

if __name__ == "__main__":
    main(createSuite())

