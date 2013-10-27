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
from WellBehavedPython.MethodSpy import *

class SampleClass:
    
    def parameterlessMethod(self):
        pass

class SpyOnTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def test_spying_on_parameterless_method(self):
        # Where
        sampleObject = SampleClass()

        # When
        spyOn(sampleObject.parameterlessMethod)

        # Then
        expect(sampleObject.parameterlessMethod
               ).toBeAnInstanceOf(MethodSpy)

    def test_can_spy_and_expect_method_to_have_been_called(self):
        # Where
        sampleObject = SampleClass()
        spyOn(sampleObject.parameterlessMethod)

        # When
        sampleObject.parameterlessMethod()

        # Then
        expect(sampleObject.parameterlessMethod).toHaveBeenCalled()        
