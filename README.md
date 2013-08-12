Well Behaved Python Tutorial
============================

Attempt to create a unit testing framework with a more fluent assertion api and set of error messages than the base python unittesting framework

Set up a test case class
------------------------

This will all be available in the example file demo.py. The framework is still undergoing active development. There is still too much boilerplate code that needs to be written to set up an then perform a test run.

First set up a test case file. We first need to import the WellBehavedPython api and TestCase classes:

~~~~~ python
from WellBehavedPython.TestCase import *
from WellBehavedPython.api import *
~~~~~

Next, set up a the test case class and constructor.

~~~~~ python
class TutorialTests(TestCase):
    def __init__(self, testName):
        TestCase.__init__(self, testName)
~~~~~

We now have an empty test case class which we can run. This is now a good time to setup the running of it using
a suite that can discover test methods in the class:

~~~~~ python
if __name__ == "__main__":
    suite = TutorialTests.suite()
    results = TestResults()
    suite.run(results)

    print(results.summary())
~~~~~

We can now run the test case, and get the useful message that we got 0 failures from zero tests
~~~~~ bash
python3 tutorial.py
0 failed from 0 test
~~~~~

A test method is any method within our test case class which starts with the word 'test'

~~~~~ python
    def test_something(self):
        pass
~~~~~

We can run this test again, and see
~~~~~ bash
python3 tutorial.py
0 failed from 1 test
~~~~~

We can set up state before tests with before and tear down state after tests with after

~~~~~ python
    def before(self):
        self.log = ["set up"]

    def test_log(self):
        self.log.append("some test")

    def after(self):
        self.log.append("tear down")	
~~~~~

Simple Assertion methods
--------------------------

The simplest asserts expect things to be true or false:

~~~~~ python
    def test_true_and_false(self):        
        expect(True).toBeTrue();
        expect(False).toBeFalse();

        # And have the same equivalent-to-true and
        # equivalent-to-false semantics as python does...
        expect(1).toBeTrue()
        expect([0]).toBeTrue()
        expect(0).toBeFalse()
        expect([]).toBeFalse()
~~~~~

These assertions lead to messages of 'Expected False to be True', or
'Expected True to be False'.

Each assertion method takes an optional parameter called userMessage
which can be used to improve the messages, and identify particular
expectations which have failed to be matched:

~~~~~ python 

    def test_add_user_message(self):
        # We can add user messages to expect calls, to identify
        # what has gone wrong more clearly
        expect(True).toBeTrue("A literal True value should be true...")
        # Failure message would be:
        # "A literal True values should be true: Expected True to be True"
~~~~~

In principle the above assertions are almost all that you need to
make tests fail. However, that is not really enough. It is far more
productive to have a really descriptive error of why things fail.

So there is a rich set of assertions, which provide better messages:

~~~~~ python
    def test_equality(self):
        expect(1).toEqual(1)
        expect("hello").toEqual("hello")
~~~~~

The reason for using the more specific assertions is for clarity of
failure message. Consider the following test with two otherwise
equivalent expectations:

~~~~~ python
    def test_good_and_bad(self):
        actual = "hello"
        expect(actual == "hello").toBeTrue() # bad
        expect(actual).toEqual("hello") # good 
~~~~~

Compare the different output: "Expected False to be True" to
"Expected 'world' to equal 'hello'". The latter makes clear what the
wrong value that actual has 
clear exactly which condition has failed.

We can also test for the opposites of conditions:

~~~~~ python

    def test_negative_conditions(self):
        expect(1).Not.toEqual(0)
        expect("hello").Not.toEqual("world")

~~~~~

If the test had world rather than hello, the error message would be
"Expected 'hello' not to equal 'world'".

Expected Exceptions
-------------------

When testing failure cases it is useful to catch certain exception types.
While this can be done with a manual try-catch block, this ends up
with a lot of boilerplate code. There is a more convenient alternative,
the toRaise() method on expect objects:

~~~~~ python
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

~~~~~

The constraint is that the function being tested must be argumentless.
Lambda expressions or inner methods are very convenient ways of doing this.
We can, of course, also use global functions:

~~~~~ python
def outer():
    raise KeyError("you are locked out")

class DemoTests(TestCase):
      # ...
      # ...
      # ...

    def test_expected_exception_inner(self):
        expect(outer).toRaise(KeyError)

~~~~~

These methods will pass if an exception of the expected type is thrown,
and fail otherwise. But sometimes the code could thrown the expected exception in more than one place, or we need to check the message being generated as well as the exception. In that case we can use either the optional expectedMessage argument (for explicit matching of full strings) or the expectedMessageMatches (which checks that the message matches the given regular expression):

~~~~~ python

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

~~~~~ 

Comparing Numbers
-----------------

When actual is a number, code for comparing numbers is used instead of the default
comparison code. This allows numeric inequality comparison operators, <, <=, > and >=
to be used. It also allows equality to be performed in the sense of the absolute
difference being within a tolerance.

The inequality operators have names that should be guessable:

~~~~~ python
    def test_that_numbers_can_be_compared_using_inequalities(self):
        actual = 1.0

        # We can use the operators > >= < and <=:
        expect(actual).toBeGreaterThan(0.0)
        expect(actual).toBeGreaterThanOrEqualTo(1.0)
        expect(actual).toBeLessThan(2.0)
        expect(actual).toBeLessThanOrEqualTo(1.0)
~~~~~

We can also write a test that demonstrates that the equality is being
performed in the sense of having a tolerance rather than being absolute:

~~~~~ python
    def test_that_equality_is_performed_within_a_tolerance(self):
        # equality for floats is performed within a tolerance
        actual = 1.00001
        expect(actual).toEqual(actual + 1e-10)
~~~~~

The tolernace can be set in equality for numbers using an optional
parameter called tolerance. The tolerance type can be set using the
toleranceType parameter, which can be 'absolute' or 'relative'.

The defaults are a tolerance of 1e-10, a toleranceType of relative.
When the tolerance is absolute, it requries that

~~~~~ 
 |actual - expected| < tolerance
~~~~~

When the tolerance type is absoulte, it requires that:

~~~~~ 
|actual - expected|
-----------------------------   < tolerance
|actual| + |expected| + 1e-20
~~~~~ 

The small factor of 1e-20 is a floor tolerance. This is to ensure that
when actual is exactly equal to expected, the result is 0 rather than NaN