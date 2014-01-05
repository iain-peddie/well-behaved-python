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
from WellBehavedPython.Engine.TestContext import TestContext

class TestContextTests(TestCase):

    def __init__(self, name):
        TestCase.__init__(self, name)

    def test_that_context_with_no_user_message_calls_expect_on_registry(self):
        # Where
        registry = self.createSpyRegistry()
        expectations = registry
        context = TestContext(registry)

        # When
        result = context.expect(5)

        # Then
        expect(registry.expect).toHaveBeenCalledWith(5)
        expect(expectations.withUserMessage).Not.toHaveBeenCalled()
        expect(result).toEqual(expectations)

    def createSpyRegistry(self):
        methods = {
            'expect': MethodSpy().andCall(lambda actual: registry),
            'withUserMessage': MethodSpy()
            }
            
        registry = type('FakeRegistry', (object,), methods)
        return registry
        
