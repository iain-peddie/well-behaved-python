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
from WellBehavedPython.Engine.TestCase import *

# Sample test cases
# These should not be run directly. They exist to be called from within the
# tests themselves.

class TestCaseWithNoTests(TestCase):
    pass

class TestCaseWithPassingTest(TestCase):
    
    def test_pass(self):
        pass

class TestCaseWithFailingTest(TestCase):

    def test_fail(self):
        expect(None).fail('Failing test')

class TestCaseWithErrorTest(TestCase):

    def test_error(self):
        raise KeyError('You are locked out')

class TestCaseWithIgnoredTest(TestCase):

    def xtest_ignore(self):
        pass

class TestCaseWithTwoPassingTests(TestCase):
    """This class should never be run directly.

    It is used to test the auto-detection of test cases."""

    def test_example1(self):
        print("test_example1")

    def test_another_example(self):
        print("test_another_example")

class TestCaseWithBeforeAndAfterClass(TestCase):

    beforeClassCalled = False
    afterClassCalled = False

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
        withUserMessage("beforeClass was not called").expect(self.beforeClassCalled).toBeTrue()
        withUserMessage("afterClass was called before test").expect(self.afterClassCalled).toBeFalse()

class TestCaseWithBeforeClassSaboteur(TestCaseWithBeforeAndAfterClass):

    @classmethod
    def beforeClass(type):
        raise KeyError("Saboteur sabotages beforeClass")

    def test_two(self):
        pass

class TestCaseWithAfterClassSaboteur(TestCaseWithBeforeAndAfterClass):

    @classmethod
    def afterClass(type):
        raise KeyError("Saboteur sabotages afterClass")

    def test_two(self):
        pass

class TestCaseWithLongTestName(TestCase):

    def test_case_with_test_name_longer_than_test_case_name(self):
        pass
