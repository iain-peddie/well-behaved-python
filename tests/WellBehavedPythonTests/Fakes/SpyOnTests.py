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
from WellBehavedPython.Fakes.MethodSpy import *

class SampleClass:

    def __init__(self):
        self.targetMethodCalled = False

    def parameterlessMethod(self):
        self.targetMethodCalled = True

class SpyOnTests(TestCase):

    def before(self):
        self.SubjectObject = SampleClass()
        spyOn(self.SubjectObject.parameterlessMethod)

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
        subjectObject = self.SubjectObject

        # When
        subjectObject.parameterlessMethod()

        # Then
        expect(subjectObject.parameterlessMethod).toHaveBeenCalled()

    def test_sample_class_is_manual_spy(self):
        # Where
        sample = SampleClass()
        before = sample.targetMethodCalled

        # When
        sample.parameterlessMethod()
        after = sample.targetMethodCalled

        # Then
        withUserMessage('called should be false initially').expect(before).toBeFalse()
        withUserMessage('called should be true after call').expect(after).toBeTrue()                

    def test_can_spy_on_and_call_through(self):
        # Where
        sample = SampleClass()
        
        # When
        spyOn(sample.parameterlessMethod).andCallThrough()
        sample.parameterlessMethod()

        # Then
        # test the spy
        expect(sample.parameterlessMethod).toHaveBeenCalled() 
        # test the callthrough
        expect(sample.targetMethodCalled).toBeTrue()
