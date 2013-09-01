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

# Sample test cases
# These should not be run directly. They exist to be called from within the
# tests themselves.

class TestCaseWithNoTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

class TestCaseWithPassingTest(TestCase):
    
    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def test_pass(self):
        pass

class TestCaseWithFailingTest(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def test_fail(self):
        expect(None).fail('Failing test')

class TestCaseWithErrorTest(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def test_error(self):
        raise KeyError('You are locked out')

class TestCaseWithIgnoredTest(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def xtest_ignore(self):
        pass

class TestCaseWithTwoPassingTests(TestCase):
    """This class should never be run directly.

    It is used to test the auto-detection of test cases."""
    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)        

    def test_example1(self):
        print("test_example1")

    def test_example2(self):
        print("test_example2")

class TestCaseWithBeforeAndAfterClass(TestCase):

    beforeClassCalled = False
    afterClassCalled = False

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)        

    @classmethod
    def beforeClass(testCase):
        testCase.beforeClassCalled = True

    @classmethod
    def afterClass(testCase):
        testCase.afterClassCalled = True

    @classmethod
    def reset(testCase):
        testCase.beforeClassCalled = False
        testCase.afterClassCalled = False

    def test_statics(self):
        expect(self.beforeClassCalled).toBeTrue("beforeClass was not called")
        expect(self.afterClassCalled).toBeFalse("afterClass was called before test")

class TestCaseWithBeforeClassSaboteur(TestCaseWithBeforeAndAfterClass):

    def __init__(self, testFunctionName):
        TestCaseWithBeforeAndAfterClass.__init__(self, testFunctionName)        

    @classmethod
    def beforeClass(type):
        raise KeyError("Saboteur sabotages beforeClass")

    def test_two(self):
        pass

class TestCaseWithAfterClassSaboteur(TestCaseWithBeforeAndAfterClass):

    def __init__(self, testFunctionName):
        TestCaseWithBeforeAndAfterClass.__init__(self, testFunctionName)        

    @classmethod
    def afterClass(type):
        raise KeyError("Saboteur sabotages afterClass")

    def test_two(self):
        pass
