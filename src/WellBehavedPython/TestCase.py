#!/usr/bin/env python3

# Copyright 2013 Iain Peddie inr314159@hotmail.com
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

import traceback
import sys

from .TestResults import TestResults
from .TestSuite import TestSuite

class TestCase:
    """Base class for TestCases. 

    At the moment, all test methods have to be in classes derived from
    TestCase. There may be a more convenient method based on decorators
    implemented in the future."""
    
    def __init__(self, testMethodName):
        """Creates an instance of this test class configured
        to run the method testMethodName in the actual test object.

        Inputs
        ------
        testMethodName: the name of the method within the class to
            run when run is called.
"""
        self.testMethod = getattr(self, testMethodName)
        self.testMethodName = testMethodName
        self.ignore = False

    def before(self):
        """Override this to create the setup logic which should run
        before each individual test method."""

    def after(self):
        """Override this to create the cleanup logic which should run
        after each individual test method."""

    def run(self, results):
        """Command to organise a single test run of a single
           test function.

           Inputs
           ------
           results : Expected to be an instance of TestResults. Runs
                     the test and calls methods on TestResults to indicate
                     the results of the test.
"""
        suiteName = ""
        results.registerTestStarted(suiteName, self.testMethodName)
        if self.ignore:
            results.registerTestIgnored(suiteName, self.testMethodName)
            return
        self.before()
        try:
            self.testMethod()
            results.registerTestPassed(suiteName, self.testMethodName)
        except AssertionError as ex:
            stackTrace = self.getStackTrace(ex)
            results.registerTestFailed(suiteName, self.testMethodName, stackTrace)
        except Exception as ex:
            stackTrace = self.getStackTrace(ex)
            results.registerTestError(suiteName, self.testMethodName, stackTrace)
        finally:
            self.after()

    def getStackTrace(self, exception):
        exInfo = sys.exc_info()
        stackInfo = traceback.extract_tb(exInfo[2])
        if len(exception.args) > 0:
            stackTrace = [exception.args[0] + "\n"]
        else:
            stackTrace = [""]
        stackTrace.extend(traceback.format_list(stackInfo))
        return stackTrace

    def handleError(self, error, errorType):
        """Handles the case of an error in running a test.

        Inputs
        ------
        error : the error condition that occurred.
        """        

        print("Test of {} encountered {}".format(self.testMethod, errorType))
        traceback.print_exc()

    def countTests(self):
        """Counts the active number of tests configured to run."""
        return 1

    @classmethod
    def beforeClass(type):
        """Default implementation of do nothing. 

        This allows classes to derive from TestCase without needing to
        define beforeClass."""
        
        pass

    @classmethod
    def suite(klass):
        """Builds a default test suite by examining the members of the class

        Inputs
        ------
        klass : the metaclass of the object being considered, e.g. TestCase

        Returns
        -------
        A test suite configured with every method which start with 'test'."""
        testMethods = [
            ];
    

        for key in klass.__dict__.keys():
            if key.startswith("test") or key.startswith("xtest"):
                testMethods.append(key)
        
        suite = TestSuite();
        for testMethod in testMethods:
            testCase = klass(testMethod)
            testCase.ignore = testMethod.startswith("x")
                
            suite.add(testCase)

        return suite



