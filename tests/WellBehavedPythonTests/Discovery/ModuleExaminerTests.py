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
from WellBehavedPython.Engine.TestCase import TestCase
from WellBehavedPython.Discovery.ModuleExaminer import ModuleExaminer

class ModuleExaminerTests(TestCase):

    def test_examiner_can_find__only_class_in_simple_module(self):
        # Where
        examiner = ModuleExaminer('WellBehavedPythonTests.Discovery.SampleModule');

        # When
        classes = examiner.listAllClasses()
        # The classes have been imported

        # Then
        from . import SampleModule
        expect(classes).toEqual([SampleModule.SampleTests])

    def test_examiner_can_find_all_classes_in_complex_module(self):
        # Where
        examiner = ModuleExaminer('WellBehavedPythonTests.Discovery.SampleComplexModule');

        # When
        classes = examiner.listAllClasses()
        # The classes have been imported

        # Then
        from . import SampleComplexModule
        expect(classes).toContain(SampleComplexModule.SampleFirstTests)
        expect(classes).toContain(SampleComplexModule.SampleSecondTests)
        expect(classes).toContain(SampleComplexModule.StandaloneClass)