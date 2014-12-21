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

from WellBehavedPython.api import *
from WellBehavedPython.Engine.TestCase import TestCase
from WellBehavedPython.Engine.TestSuite import TestSuite
from WellBehavedPython.Discovery.TestDiscoverer import TestDiscoverer

class TestDiscovererTests(TestCase):

    def test_can_find_only_TestCase_in_a_module(self):
        # Where
        discoverer = TestDiscoverer();
        moduleName = 'WellBehavedPythonTests.Discovery.Samples.SampleModule'

        # When
        suite = discoverer.buildSuiteFromModuleName(moduleName)
        
        # Then
        expect(suite).toBeAnInstanceOf(TestSuite)
        expect(suite.countTests()).toEqual(1)
        expect(suite.suiteName).toEqual(moduleName)
        expect(suite.tests[0]).toBeAnInstanceOf(TestSuite)
        childSuite = suite.tests[0]
        expect(childSuite.suiteName).toEqual('SampleTests')

    def test_can_find_multiple_TestCases_in_a_module(self):
        # Where
        discoverer = TestDiscoverer();
        moduleName = 'WellBehavedPythonTests.Discovery.Samples.SampleComplexModule'

        # When
        suite = discoverer.buildSuiteFromModuleName(moduleName)
        
        # Then
        expect(suite).toBeAnInstanceOf(TestSuite)
        expect(suite.countTests()).toEqual(2)
        expect(suite.suiteName).toEqual(moduleName)

        expect(suite.tests[0]).toBeAnInstanceOf(TestSuite)
        firstChildSuite = suite.tests[0]
        expect(firstChildSuite.suiteName).toEqual('SampleFirstTests')

        expect(suite.tests[1]).toBeAnInstanceOf(TestSuite)
        secondChildSuite = suite.tests[1]
        expect(secondChildSuite.suiteName).toEqual('SampleSecondTests')

    def test_class_suite_returned_when_only_one_class_and_class_name_matches_module_name(self):
        # Where
        discoverer = TestDiscoverer();
        moduleName = 'WellBehavedPythonTests.Discovery.Samples.SampleClass'

        # When
        suite = discoverer.buildSuiteFromModuleName(moduleName)
        
        # Then
        expect(suite).toBeAnInstanceOf(TestSuite)
        expect(suite.countTests()).toEqual(1)
        expect(suite.suiteName).toEqual('SampleClass')
        expect(suite.tests[0]).toBeAnInstanceOf(TestCase)
        childCase = suite.tests[0]
        expect(childCase.testMethodName).toEqual("test_sample")

    def test_all_modules_returned_when_discovering_on_a_package(self):
        # Where
        discoverer = TestDiscoverer();
        moduleName = 'WellBehavedPythonTests.Discovery.Samples'

        # When
        suite = discoverer.buildSuiteFromModuleName(moduleName)
        
        # Then
        testsInExtendedModule = 2
        testsInSimpleModule = 1
        testsInSimpleClass = 1
        numExpectedTests = testsInExtendedModule + testsInSimpleModule + testsInSimpleClass
        expect(suite).toBeAnInstanceOf(TestSuite)
        expect(suite.countTests()).toEqual(numExpectedTests)
        expect(suite.suiteName).toEqual(moduleName)
        expect(suite.tests[0]).toBeAnInstanceOf(TestSuite)
        
        expectedChildren = { 'SampleModule': 1, 
                             'SampleComplexModule': 2,
                             'SampleClass' : 1}


        self.assertIsSuiteWith(suite.tests[0], expectedChildren)
        self.assertIsSuiteWith(suite.tests[1], expectedChildren)
        self.assertIsSuiteWith(suite.tests[2], expectedChildren)

    def assertIsSuiteWith(self, suite, childrenDict):
        expect(suite).toBeAnInstanceOf(TestSuite)
        expect(childrenDict).toContainKey(suite.suiteName)
        expect(len(suite.tests)).toEqual(childrenDict[suite.suiteName]);
        

