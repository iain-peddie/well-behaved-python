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
from WellBehavedPython.MethodSpy import *

from .SampleTestCases import *

import io

class MethodSpyTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def before(self):
        self.spy = MethodSpy()

    def test_setup(self):
        pass

    def test_that_uncalled_spy_hasBeenCalled_returns_False(self):
        # Where
        spy = self.spy

        # When

        # Then
        expect(spy.hasBeenCalled()).toBeFalse()

    def test_that_uncalled_spy_getNumberOfCalls_returns_0(self):
        # Where
        spy = self.spy

        # When

        # Then
        expect(spy.getNumberOfCalls()).toEqual(0)

    def test_that_called_spy_hasBeenCalled_returns_True(self):
        # Where
        spy = self.spy

        # When
        spy()

        # Then
        expect(spy.hasBeenCalled()).toBeTrue("Called spy should claim to have been called")

    def test_that_spy_called_once_getNumberOfCalls_returns_1(self):
        # Where
        spy = self.spy

        # When
        spy()

        # Then
        expect(spy.getNumberOfCalls()).toEqual(1, "Number of calls")
        
    def test_that_spy_called_twice_getNumberOfCalls_returns_2(self):
        # Where
        spy = self.spy

        # When
        spy()
        spy()

        # Then
        expect(spy.getNumberOfCalls()).toEqual(2, "Number of calls")

    def test_that_spy_description_is_based_on_methodName(self):
        # Where
        anonymousSpy = self.spy
        namedSpy= MethodSpy(methodName = "test_function")

        # Then
        expect(anonymousSpy.getDescription()).toEqual("<anonymous>")
        expect(namedSpy.getDescription()).toEqual("<test_function>")        
        

