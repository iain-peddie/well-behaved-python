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
from WellBehavedPython.api import *
from WellBehavedPython.ExpectationsRegistry import *

class ExpectationsFactoryTests(TestCase):

    def __init__(self, name):
        TestCase.__init__(self, name)

    def test_that_factory_says_should_not_create_when_predicate_is_False(self):
        # Where
        factory = ExpectationsFactory(lambda typeName: False, None)

        # When
        result = factory.shouldCreateFor(int)

        # Then
        expect(result).toBeFalse()
        
