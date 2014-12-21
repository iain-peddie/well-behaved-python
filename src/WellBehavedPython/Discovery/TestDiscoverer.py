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

class TestDiscoverer:
    """Class used to find tests given a package.
    
    Uses ModuleExaminer to determine classes in modules, modules and subpackages in packages,
    and traverses them to find classes derived from TestCase."""

    def buildSuiteFromModuleName(self, moduleName):
        from ..Engine.TestSuite import TestSuite
        from .ModuleExaminer import ModuleExaminer

        suite = TestSuite(moduleName)
        examiner = ModuleExaminer(moduleName)

        for item in examiner.listAllClasses():
            suite.add(item.suite())
        
        return suite
