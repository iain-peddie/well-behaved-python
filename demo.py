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

# import the API
from WellBehavedPython.TestCase import *
from WellBehavedPython.api import *

def outer():
    raise KeyError("you are locked out")


# derive a class from TestCase and call the base class constructor
class DemoTests(TestCase):
    def __init__(self, testName):
        TestCase.__init__(self, testName)

    # any method starting with test is a test
    def test_something(self):
        pass

    # we can set up state for tests
    def before(self):
        self.log = ["set up"]

    def test_log(self):
        self.log.append("some test")

    # And tear it down
    def after(self):
        self.log.append("tear down")
        # this log would contain ["set up", "some test", "tear down"]

    def test_true_and_false(self):        
        # We can expect things to be true or false
        expect(True).toBeTrue();
        expect(False).toBeFalse();

        # And have the same equivalent-to-true and
        # equivalent-to-false semantics as python does...
        expect(1).toBeTrue()
        expect([0]).toBeTrue()
        expect(0).toBeFalse()
        expect([]).toBeFalse()

    def test_add_user_message(self):
        # We can add user messages to expect calls, to identify
        # what has gone wrong more clearly
        expect(True).toBeTrue("A literal True value should be true...")
        # Failure message would be:
        # "A literal True values should be true: Expected True to be True"

    def test_equality(self):
        # We can test for equality
        expect(1).toEqual(1)
        expect("hello").toEqual("hello")

    def test_negative_conditions(self):
        # We can test the opposites of conditions
        expect(1).Not.toEqual(0)
        expect("hello").Not.toEqual("world")

    def test_expected_exceptions_lambda(self):
        # We can expect exceptions to happen, using lambda
        # expressions
        expect(lambda: expect(True).toBeFalse()).toRaise(
            AssertionError)

    def test_expected_exception_inner(self):
        # We can use nested functions as well
        def inner():
            raise KeyError("you are locked out")

        expect(inner).toRaise(KeyError)

    def test_expected_exception_inner(self):
        # We can also, of course, use global scope functions
        expect(outer).toRaise(KeyError)

    def test_expected_exception_exact_message(self):
        # We can match exception messages as well
        expect(outer).toRaise(KeyError, 
                              expectedMessage = "you are locked out")

    def test_expected_exception_message_matches(self):
        # We can use regular expressions to match
        # parts of exception messages:
        expect(outer).toRaise(KeyError, expectedMessageMatches = "lock.d")

        # And we can use compiled regular expressions as well:

        import re
        regexp = re.compile("you.*out")
        expect(outer).toRaise(KeyError, expectedMessageMatches = regexp)
        
    




# create a main that calls the test case:

if __name__ == "__main__":
    suite = DemoTests.suite()
    results = TestResults()
    suite.run(results)

    print(results.summary())
