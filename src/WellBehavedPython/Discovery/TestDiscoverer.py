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
        
        Parameters
        ----------
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

        self.addTestCasesToSuite(suite, examiner, moduleName)
        suite = self.simplifySuite(suite, moduleName)
        self.addModulesToSuite(suite, examiner, ignoreFilters)
        
        return suite


    def addTestCasesToSuite(self, suite, examiner, moduleName):

        subSuite = []

        for item in examiner.listAllClasses():
            if issubclass(item, TestCase):
                subSuite = item.suite()
                suite.add(subSuite)

    def addModulesToSuite(self, suite, examiner, ignoreFilters):
        modules = examiner.listAllModules()
        for module in modules:
            subsuiteName = self._getLastPartOfModuleName(module)
            suite.add(self.buildSuiteFromModuleName(module, subsuiteName, ignoreFilters = ignoreFilters))


    def simplifySuite(self, suite, moduleName):

        uniqueModuleName = self._getLastPartOfModuleName(moduleName)


        if len(suite.tests) == 1 and suite.tests[0].suiteName == uniqueModuleName:
            return suite.tests[0]

        return suite

    def _getLastPartOfModuleName(self, moduleName):
        moduleParts = moduleName.split(".")
        return moduleParts[-1]
