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

from WellBehavedPython.TestCase import *
from WellBehavedPython.MethodSpy import MethodSpy
from WellBehavedPython.api import *
from WellBehavedPython.MethodSpyExpectations import MethodSpyExpectations
from WellBehavedPython.BaseExpect import BaseExpect

class MethodSpyExpectationsTests(TestCase):

    def __init__(self, name):
        TestCase.__init__(self, name)

    def test_spy_expectations_registered_for_spies_by_default(self):
        # Where
        spy = MethodSpy()
        
        # When
        expecter = expect(spy)

        # Then
        expect(expecter).toBeAnInstanceOf(MethodSpyExpectations)
        expect(expecter).toBeAnInstanceOf(BaseExpect)
