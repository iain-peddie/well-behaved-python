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

from ..Engine.TestSuite import TestSuite
from ..Engine.TestCase import TestCase
from .ModuleExaminer import ModuleExaminer
import re

class TestDiscoverer:
    """Class used to find tests given a package.
    
    Uses ModuleExaminer to determine classes in modules, modules and subpackages in packages,
    and traverses them to find classes derived from TestCase."""

    def buildSuiteFromModuleName(self, moduleName, suiteName = None, ignoreFilters=[]):
        """Builds a test suite given a module or package name.
        
        Inputs
        ------

        moduleName : [str] The name of the module to examine
        suiteName : [str] The name of the suite. If None, the moduleName will be used as
             the suite name
        filter:  [iterable of str] Ignore filter. Modules matching these filters will be ignored."""
        

        if suiteName is None:
            suiteName = moduleName

        examiner = ModuleExaminer(moduleName) 

        suite = TestSuite(suiteName)    

        for nextFilter in ignoreFilters:
            if re.search(nextFilter, moduleName):                
                return suite

        self.addTestCasesToSuite(suite, examiner)
        suite = self.simplifySuite(suite, moduleName)
        self.addModulesToSuite(suite, examiner, ignoreFilters)
        
        return suite


    def addTestCasesToSuite(self, suite, examiner):
        """Given a test suite and a module name add the test class subsuites.

        Iterate over a module, find all the classes derived from TestCase, and
        use their autosuite generation to create new subsites, which get added to suite. 

        Inputs
        ------
        suite : The [TestSuite] to add child suites to
        examiner : The [ModuleExaminer] to use to find children."""
        subSuite = []

        for item in examiner.listAllClasses():
            if issubclass(item, TestCase):
                subSuite = item.suite()
                suite.add(subSuite)

    def addModulesToSuite(self, suite, examiner, ignoreFilters):
        """Given a test suite and a module examiner add direct child modules to the suite.

        Inputs
        ------
        suite : The [TestSuite] suite to add subsuite to
        examiner : The [MoudleExaminer] examiner to find modules for. If this is not examining a 
            package, no modules will be found
        ignoreFilters The [iterable of str] list of regular expression filters to apply to module
            names. Any module name which is matched will be filtered out of the final suite."""

        modules = examiner.listAllModules()
        for module in modules:
            subsuiteName = self._getLastPartOfModuleName(module)
            subsuite = self.buildSuiteFromModuleName(module, subsuiteName, ignoreFilters = ignoreFilters) 
            if subsuite.countTests() > 0:
                suite.add(subsuite)


    def simplifySuite(self, suite, moduleName):
        """Simplifies the suite

        Post-processes suites so that modules with a single test case class where the test case
        class has the same name as the module get converted so that the tests are put in the top
        level suite, rather than a subsuite.

        Inputs
        ------
        suite : The [TestSuite]  to simplify
        moduleName : The [str] name of the module corresponding to the suite."""

        uniqueModuleName = self._getLastPartOfModuleName(moduleName)


        if len(suite.tests) == 1 and suite.tests[0].suiteName == uniqueModuleName:
            return suite.tests[0]

        return suite

    def _getLastPartOfModuleName(self, moduleName):
        moduleParts = moduleName.split(".")
        return moduleParts[-1]
