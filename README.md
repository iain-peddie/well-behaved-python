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

A test method is any method which starts with the word 'test'

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
        # We can test for equality
        expect(1).toEqual(1)
        expect("hello").toEqual("hello")
~~~~~

Compare the different output: "Expected True to be False", to
"Expected 'world' to equal 'hello'". The latter usually makes abundantly
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

TODO