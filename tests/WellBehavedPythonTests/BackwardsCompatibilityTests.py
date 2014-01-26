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

# this imports the new test case class
from WellBehavedPython.Engine.TestCase import *

import warnings

            
class BackwardsCompatibilityTests(TestCase):

    def test_that_importing_old_module_raises_a_DeprecationWarning(self):
        # Where
        with warnings.catch_warnings(record = True) as warn:
            warnings.simplefilter("always")
            
            # When
            import WellBehavedPython.TestCase

            # Then
            withUserMessage('expected a warning on module import').expect(len(warn)).toEqual(1)
            importWarning = warn[-1]
            expect(issubclass(importWarning.category, DeprecationWarning)).toBeTrue()
            expect(str(importWarning.message)).toMatch('deprecated')

    def test_running_using_old_testcase_class_works(self):

        import WellBehavedPython.TestCase

        class OldTestCase(WellBehavedPython.TestCase.TestCase):

            def __init__(this, name):
                WellBehavedPython.TestCase.TestCase.__init__(this, name)
        
                def test_that_passes(this):
                    pass

        # Where
        testClass = OldTestCase("test_that_passes")
        results = TestResults()

        # When        
        testClass.run(results)

        # Then
        expect(results.countTests()).toEqual(1)
