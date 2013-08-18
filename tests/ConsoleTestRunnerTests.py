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

from WellBehavedPython.api import *
from WellBehavedPython.TestCase import *
from WellBehavedPython.ConsoleTestRunner import *

import io

class TestCaseWithNoTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

class TestCaseWithOneTest(TestCase):
    
    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def test_one(self):
        pass


class TestCaseWithTwoTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def test_two(self):
        expect(True).toBeFalse();

    def test_three(self):
        pass
    
class ConsoleTestRunnerTests(TestCase):
    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def test_that_running_suite_with_no_tests_produces_correct_output(self):
        # Where
        runnerIo = io.StringIO();
        runner = ConsoleTestRunner(runnerIo)
        suite = TestCaseWithNoTests.suite()

        # When
        runner.run(suite)

        # Then
        expect(runnerIo.getvalue()).toMatch("""Starting test run of 0 tests
0 failed from 0 tests""")
        
        
