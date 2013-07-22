Well Behaved Python
===================

Attempt to create a unit testing framework with a more fluent assertion api and set of error messages than the base python unittesting framework

Tutorial
--------

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
        TestCase.__init__(testName)
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
