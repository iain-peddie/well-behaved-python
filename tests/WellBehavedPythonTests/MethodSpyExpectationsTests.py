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
from WellBehavedPython.MethodSpy import MethodSpy
from WellBehavedPython.api import *
from WellBehavedPython.MethodSpyExpectations import MethodSpyExpectations
from WellBehavedPython.BaseExpect import BaseExpect

class MethodSpyExpectationsTestsBase(TestCase):
    def __init__(self, name):
        TestCase.__init__(self, name)

    def createMethodSpyWhichHasNotBeenCalled(self):
        spy = MethodSpy()
        return spy

    def createMethodSpyWhichHasBeenCalled(self):
        spy = self.createMethodSpyWhichHasNotBeenCalled()
        self.call(spy)
        return spy

    def call(self, spy):
        spy()


class MethodSpyExpectationsTests(MethodSpyExpectationsTestsBase):
    def __init__(self, name):
        MethodSpyExpectationsTestsBase.__init__(self, name)

    def test_spy_expectations_registered_for_spies_by_default(self):
        # Where
        spy = MethodSpy()
        
        # When
        expecter = expect(spy)

        # Then
        expect(expecter).toBeAnInstanceOf(MethodSpyExpectations)
        expect(expecter).toBeAnInstanceOf(BaseExpect)

    def test_expect_method_called_passes_when_method_has_been_called(self):
        # Where
        calledSpy = self.createMethodSpyWhichHasBeenCalled()

        # Then
        expect(calledSpy).toHaveBeenCalled()

    def test_expect_method_called_fails_when_method_has_not_been_called(self):
        # Where
        uncalledSpy = self.createMethodSpyWhichHasNotBeenCalled()
        
        # Then
        expect(lambda: expect(uncalledSpy).toHaveBeenCalled()).toRaise(
            AssertionError, 
            expectedMessage = 'Expected <anonymous> to have been called')

    def test_expect_method_called_twice_passes_when_method_has_been_called_twice(self):
        # Where
        calledSpy = self.createMethodSpyWhichHasBeenCalled()
        self.call(calledSpy)

        # Then
        expect(calledSpy).toHaveBeenCalled(times = 2)

    def test_expect_method_called_twice_failed_if_spy_only_called_once(self):
        # Where
        calledSpy = self.createMethodSpyWhichHasBeenCalled()

        # Then
        expect(lambda: expect(calledSpy).toHaveBeenCalled(times = 2)).toRaise(
            AssertionError,
            expectedMessage = 'Expected <anonymous> to have been called 2 times')

    def test_expect_method_called_twice_failed_if_spy_only_called_three_times(self):
        # Where
        calledSpy = self.createMethodSpyWhichHasBeenCalled()
        self.call(calledSpy)
        self.call(calledSpy)

        # Then
        expect(lambda: expect(calledSpy).toHaveBeenCalled(times = 2)).toRaise(
            AssertionError,
            expectedMessage = 'Expected <anonymous> to have been called 2 times')

    def test_expect_toHaveBeenCalled_with_usermessage(self):
        # Where
        uncalledSpy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        # do nothing

        # Then
        expect(lambda:
                   expect(uncalledSpy).toHaveBeenCalled(userMessage = "userMessage")).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage:")

    def test_expect_toHaveBeenCalled_1_times_message(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()
        
        # When

        # Then
        expect(lambda:
                   expect(spy).toHaveBeenCalled(times = 1)).toRaise(
            AssertionError, 
            expectedMessage = "Expected <anonymous> to have been called 1 time")


class MethodSpyNotExpectationsTests(MethodSpyExpectationsTestsBase):

    def __init__(self, name):
        MethodSpyExpectationsTestsBase.__init__(self, name)

    def test_expect_method_not_called_fails_when_method_has_been_called(self):
        # Where
        calledSpy = self.createMethodSpyWhichHasBeenCalled()

        # Then
        expect(lambda: expect(calledSpy).Not.toHaveBeenCalled()).toRaise(
            AssertionError, 
            expectedMessage = 'Expected <anonymous> not to have been called')
            

    def test_expect_method_not_called_passes_when_method_has_not_been_called(self):
        # Where
        uncalledSpy = self.createMethodSpyWhichHasNotBeenCalled()
        
        # Then
        expect(uncalledSpy).Not.toHaveBeenCalled()

    def test_expect_called_with_passes_when_matching_one_call_exactly(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(1)

        # Then
        expect(spy).toHaveBeenCalledWith(1) # not to raise

