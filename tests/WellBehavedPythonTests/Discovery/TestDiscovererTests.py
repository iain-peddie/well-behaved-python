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
        moduleName = 'WellBehavedPythonTests.Samples.SampleModule'

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
        moduleName = 'WellBehavedPythonTests.Samples.SampleComplexModule'

        # When
        suite = discoverer.buildSuiteFromModuleName(moduleName)
        
        # Then
        expect(suite).toBeAnInstanceOf(TestSuite)
        expect(suite.countTests()).toEqual(4)
        expect(suite.suiteName).toEqual(moduleName)

        expectedChildren = { 'SampleFirstTests': 1, 
                             'SampleSecondTests': 1,
                             'SampleDerivedTests' : 2}


        self.assertIsSuiteWith(suite.tests[0], expectedChildren)
        self.assertIsSuiteWith(suite.tests[1], expectedChildren)
        self.assertIsSuiteWith(suite.tests[2], expectedChildren)

    def test_class_suite_returned_when_only_one_class_and_class_name_matches_module_name(self):
        # Where
        discoverer = TestDiscoverer();
        moduleName = 'WellBehavedPythonTests.Samples.SampleClass'

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
        moduleName = 'WellBehavedPythonTests.Samples'

        # When
        suite = discoverer.buildSuiteFromModuleName(moduleName)
        
        # Then
        testsInExtendedModule = 2
        testsInSimpleModule = 1
        testsInSimpleClass = 1
        testsInSampleTestCases = 10
        leastNumExpectedTests = testsInExtendedModule + testsInSimpleModule + testsInSimpleClass + testsInSampleTestCases
        expect(suite).toBeAnInstanceOf(TestSuite)
        expect(suite.countTests()).toBeGreaterThanOrEqualTo(leastNumExpectedTests)
        expect(suite.suiteName).toEqual(moduleName)
        expect(suite.tests[0]).toBeAnInstanceOf(TestSuite)
        
        expectedChildren = { 'SampleModule': 1, 
                             'SampleComplexModule': 3,
                             'SampleClass' : 1}


        self.assertIsSuiteWith(suite.tests[0], expectedChildren)
        self.assertIsSuiteWith(suite.tests[1], expectedChildren)
        self.assertIsSuiteWith(suite.tests[2], expectedChildren)

    def test_discovery_recurses_into_subpackages(self):
        # Where
        discoverer = TestDiscoverer();
        moduleName = 'WellBehavedPythonTests'

        # When
        suite = discoverer.buildSuiteFromModuleName(moduleName)
        
        # Then
        expectedLowerLimitOnTests = 400
        expect(suite).toBeAnInstanceOf(TestSuite)
        expect(suite.countTests()).toBeGreaterThanOrEqualTo(expectedLowerLimitOnTests)
        expect(suite.suiteName).toEqual(moduleName)
        expect(suite.tests[0]).toBeAnInstanceOf(TestSuite)
        
        expectedChildren = { 'Samples' : 4 }
        found = False
        for test in suite.tests:
            if test.suiteName == 'Samples':
                self.assertIsSuiteWith(test, expectedChildren)
                found = True
                break

        withUserMessage('Expected a subsuite with a name of "Samples"').expect(found).toBeTrue()

    
    def test_discovery_recurses_into_subpackages(self):
        # Where
        discoverer = TestDiscoverer();
        moduleName = 'WellBehavedPythonTests'

        # When
        suite = discoverer.buildSuiteFromModuleName(moduleName, ignoreFilters=['Samples'])
        
        # Then
        expectedLowerLimitOnTests = 400
        expect(suite).toBeAnInstanceOf(TestSuite)
        expect(suite.countTests()).toBeGreaterThanOrEqualTo(expectedLowerLimitOnTests)
        expect(suite.suiteName).toEqual(moduleName)
        expect(suite.tests[0]).toBeAnInstanceOf(TestSuite)
        
        found = False
        for test in suite.tests:
            if test.suiteName == 'Samples':
                self.assertIsSuiteWith(test, expectedChildren)
                found = True
                break

        withUserMessage('Expected samples subsuite to be filtered').expect(found).toBeFalse()
        

    def test_can_filter_out_single_module(self):
        # Where
        discoverer = TestDiscoverer();
        moduleName = 'WellBehavedPythonTests.Samples'

        # When
        suite = discoverer.buildSuiteFromModuleName(moduleName, ignoreFilters=['TestCases'])
        
        # Then
        testsInExtendedModule = 2
        testsInSimpleModule = 1
        testsInSimpleClass = 1
        leastNumExpectedTests = testsInExtendedModule + testsInSimpleModule + testsInSimpleClass

        expect(suite).toBeAnInstanceOf(TestSuite)
        expect(suite.countTests()).toBeGreaterThanOrEqualTo(leastNumExpectedTests)
        expect(suite.suiteName).toEqual(moduleName)
        expect(suite.tests[0]).toBeAnInstanceOf(TestSuite)
        
        expectedChildren = { 'SampleModule': 1, 
                             'SampleComplexModule': 3,
                             'SampleClass' : 1}


        self.assertIsSuiteWith(suite.tests[0], expectedChildren)
        self.assertIsSuiteWith(suite.tests[1], expectedChildren)
        self.assertIsSuiteWith(suite.tests[2], expectedChildren)

    def test_modules_filtered_with_multiple_filters(self):
        # Where
        discoverer = TestDiscoverer();
        moduleName = 'WellBehavedPythonTests.Samples'

        # When
        suite = discoverer.buildSuiteFromModuleName(moduleName, ignoreFilters=['Complex', 'TestCases'])
        
        # Then
        testsInSimpleModule = 1
        testsInSimpleClass = 1
        numExpectedTests = testsInSimpleModule + testsInSimpleClass

        expect(suite).toBeAnInstanceOf(TestSuite)
        expect(suite.countTests()).toEqual(numExpectedTests)
        expect(suite.suiteName).toEqual(moduleName)
        expect(suite.tests[0]).toBeAnInstanceOf(TestSuite)
        
        expectedChildren = { 'SampleModule': 1, 
                             'SampleClass' : 1}


        self.assertIsSuiteWith(suite.tests[0], expectedChildren)
        self.assertIsSuiteWith(suite.tests[1], expectedChildren)

    def test_classnames_are_filtered(self):
        # Where
        discoverer = TestDiscoverer();
        moduleName = 'WellBehavedPythonTests.Samples.SampleComplexModule'

        # When
        suite = discoverer.buildSuiteFromModuleName(moduleName, ignoreFilters=['First'])
        
        # Then
        testsInModule = 2
        testsMatchingFilter = 1
        numExpectedTests = testsInModule - testsMatchingFilter

        expect(suite).toBeAnInstanceOf(TestSuite)
        expect(suite.countTests()).toEqual(numExpectedTests)
        expect(suite.suiteName).toEqual(moduleName)
        expect(suite.tests[0]).toBeAnInstanceOf(TestSuite)
        
        expectedChildren = { 'SampleSecondTests': 1}

        self.assertIsSuiteWith(suite.tests[0], expectedChildren)                

    def test_classnames_are_filtered(self):
        # Where
        discoverer = TestDiscoverer();
        moduleName = 'WellBehavedPythonTests.Samples.SampleTestCases'

        # When
        suite = discoverer.buildSuiteFromModuleName(moduleName, 
                                                    ignoreFilters=['Saboteur', 'Passing'])
        
        # Then
        testsInModule = 9
        testsMatchingFirstFilter = 2
        testsMatchingSecondFilter = 2
        numExpectedTests = testsInModule - (testsMatchingFirstFilter + testsMatchingSecondFilter)

        expect(suite).toBeAnInstanceOf(TestSuite)
        expect(suite.countTests()).toEqual(numExpectedTests)
        expect(suite.suiteName).toEqual(moduleName)
        expect(suite.tests[0]).toBeAnInstanceOf(TestSuite)
        
        expectedChildren = { 'TestCaseWithFailingTest' : 1, 
                             'TestCaseWithErrorTest' : 1,
                             'TestCaseWithIgnoredTest' : 1,
                             'TestCaseWithBeforeAndAfterClass' : 1,
                             'TestCaseWithLongTestName' : 1 }

        for iChild in range(len(expectedChildren)):
            self.assertIsSuiteWith(suite.tests[iChild], expectedChildren)                

    def test_filter_constraining_module_and_class_name_applied(self):
        # Where
        discoverer = TestDiscoverer();
        moduleName = 'WellBehavedPythonTests.Samples.SampleComplexModule'

        # When
        suite = discoverer.buildSuiteFromModuleName(moduleName, ignoreFilters=['Samples.*First'])
        
        # Then
        testsInModule = 4
        testsMatchingFilter = 1
        numExpectedTests = testsInModule - testsMatchingFilter

        expect(suite).toBeAnInstanceOf(TestSuite)
        expect(suite.countTests()).toEqual(numExpectedTests)
        expect(suite.suiteName).toEqual(moduleName)
        expect(suite.tests[0]).toBeAnInstanceOf(TestSuite)
        
        expectedChildren = { 'SampleSecondTests': 1,
                             'SampleDerivedTests' : 2}

        self.assertIsSuiteWith(suite.tests[0], expectedChildren)                
        self.assertIsSuiteWith(suite.tests[1], expectedChildren)                

        

    def assertIsSuiteWith(self, suite, childrenDict):
        expect(suite).toBeAnInstanceOf(TestSuite)
        expect(childrenDict).toContainKey(suite.suiteName)
        expect(len(suite.tests)).toEqual(childrenDict[suite.suiteName]);
        

