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

from WellBehavedPython.TestCase import *
from WellBehavedPython.TestResults import *
from WellBehavedPython.TestResult import *
from WellBehavedPython.api import *

from datetime import *

class TestResultTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def before(self):
        self.results = TestResult("TestResultTests", "before")

    def test_before(self):
        expect(self.results.SuiteName).toEqual("TestResultTests")
        expect(self.results.TestName).toEqual("before")

    def test_register_test_started_stores_starttime(self):
        # Where
        results = self.results
        timeNow = datetime.now()

        # When
        results.registerTestStarted()

        # Then
        expect(results.StartTime).toBeGreaterThan(timeNow)

    def test_register_testEnds_all_fail_if_test_not_started(self):
        # Where
        results = self.results

        # Then
        expect(lambda: results.registerTestPassed()).toRaise(
            AssertionError,
            expectedMessage = "Unstarted test registered as passed")
        
        expect(lambda: results.registerTestIgnored()).toRaise(
            AssertionError,
            expectedMessage = "Unstarted test registered as ignored")

        expect(lambda: results.registerTestFailed(["stacktrace"])).toRaise(
            AssertionError,
            expectedMessage = "Unstarted test registered as failed")

        expect(lambda: results.registerTestError(["stacktrace"])).toRaise(
            AssertionError,
            expectedMessage = "Unstarted test registered as error")
        
    def test_that_register_test_finished_registers_finish_time(self):
        # Where
        results = self.results
        start = datetime.now()
        results.registerTestStarted()

        # When
        results.registerTestFinished("")

        # Then
        end = datetime.now()
        expect(results.EndTime).toBeGreaterThanOrEqualTo(results.StartTime)
        expect(results.EndTime).toBeLessThanOrEqualTo(end)

        expect(results.getDuration()).toBeLessThan(end - start)

        
