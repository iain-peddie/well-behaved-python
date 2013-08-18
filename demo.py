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

    ## Truth comparisons

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

    ## Expected Exceptions

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
        
    ## Numeric comparisons

    def test_equality(self):
        # We can test for equality
        expect(1).toEqual(1)
        expect("hello").toEqual("hello")

    def test_negative_conditions(self):
        # We can test the opposites of conditions
        expect(1).Not.toEqual(0)
        expect("hello").Not.toEqual("world")

    def test_that_numbers_can_be_compared_using_inequalities(self):
        actual = 1.0

        # We can use the operators > >= < and <=:
        expect(actual).toBeGreaterThan(0.0)
        expect(actual).toBeGreaterThanOrEqualTo(1.0)
        expect(actual).toBeLessThan(2.0)
        expect(actual).toBeLessThanOrEqualTo(1.0)

    def test_that_equality_is_performed_within_a_tolerance(self):
        # equality for floats is performed within a tolerance
        actual = 1.00001
        expect(actual).toEqual(actual + 1e-10)

    def test_that_equality_tolerance_can_be_configured(self):
        actual = 1
        # we can reset the tolerance level
        expect(actual).toEqual(1.01, tolerance=0.1)
        # We can also reset the tolerance type to be aboslute rather
        # than relative
        expect(actual).toEqual(10, tolerance = 10, toleranceType = 'absolute')

    ## Containers
        
    # Containers can be compared
    def test_that_containers_can_be_compared(self):
        actual = (1, 2, 3)
        # We can compare containers
        expect(actual).toEqual((1, 2, 3))
        expect(list(actual)).toEqual([1, 2, 3])

    def test_that_similar_containers_can_be_compared(self):
        actual = (1, 2, 3)
        expect(actual).toEqual([1, 2, 3])

    def test_that_container_contents_can_be_expected(self):
        # We can also expect that containers contain something
        actual = (1, 2, 3)
        expect(actual).toContain(2)

    def test_that_set_relations_can_be_expected(self):
        # We can also expect the actual to be a superset or
        # a subset of another container. This generalises
        # the pyhton sets, so that set comparisons can work
        # on lists and tuples:
        actual = (1,2,3) # a tuple
        expect(actual).toBeASupersetOf([2]) 
        expect(actual).toBeASubsetOf([0,1,2,3,4])        

    ## Dictionary Expectations

    def test_dictionary_equality(self):
        # Dictionaries can be compared. The failure message
        # then knows it is a dictionary being compared and
        # adds some more useful information to help understand
        # the cause of the failure.
        actual = {"a" : 1,
                  "b" : 2 }

        expect(actual).toEqual({"a":1, "b":2})

    def test_dictionary_contains_key(self):
        # Whether a dictionary contains a key is a useful test,
        # and having a method for it can give a more
        # enlightening error message than using a container
        # comparison on the keys view:
        actual = {"a" : 1, 
                  "b" : 2}

        expect(actual).toContainKey("a")
        expect(actual).Not.toContainKey(1)

    def test_dictionary_contains_value(self):
        # Whether a dictionary contains a value is also a useful
        # test, and gives a more enlightening message than using
        # a conainer comparison on the values view.
        actual = {"a" : 1, 
                  "b" : 2}

        expect(actual).toContainValue(1)
        expect(actual).Not.toContainValue("a")
        
    def test_evil(self):
        actual = { "a" : 1, "b" : 2}
        expect(actual).toContainValue(26)

# create a main that calls the test case:

if __name__ == "__main__":
    suite = DemoTests.suite()
    results = TestResults()
    suite.run(results)

    print(results.summary())
