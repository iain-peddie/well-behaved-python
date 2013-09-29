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

We now have an empty test case class which we can run. This is now a good time to setup the running of it using a suite that can discover test methods in the class. 

~~~~~ python
from WellBehavedPython.TestSuite import *
from WellBehavedPython.VerboseConsoleTestRunner import *
from TutorialTests import *

if __name__ == "__main__":
    suite = TestSuite("all tests")
    suite.add(TutorialTests.suite())
    # add other suites using TestCaseClass.suite()

    runner = VerboseConsoleTestRunner(bufferOutput = True)
    results = runner.run(suite)    
~~~~~

In the above test, we chose to run using the VerboseConsoleTestRunner. There is also a ConsoleTestRunner, which produces less verbose output.

We can now run the test case, and get the useful message that we got 0 failures from zero tests
~~~~~ bash
python3 tutorial.py
all tests...
   TutorialTests...
   TutorialTests... passed in 0.000s
all tests.......... passed in 0.000s
0 failed 0 errors 0 ignored from 0 tests
~~~~~

A test method is any method within our test case class which starts with the word 'test'

~~~~~ python
    def test_something(self):
        pass
~~~~~

We can run this test again, and see
~~~~~ bash
python3 tutorial.py
python3 tutorial.py
all tests...............
   TutorialTests........
      test_something ... passed in 0.001s
   TutorialTests........ passed in 0.002s
all tests............... passed in 0.003s
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

We can use this to write a test with a much looser tolernace:

~~~~~ python
    def test_that_equality_tolerance_can_be_configured(self):
        actual = 1
        # we can reset the tolerance level
        expect(actual).toEqual(1.01, tolerance=0.1)
        # We can also reset the tolerance type to be aboslute rather
        # than relative
        expect(actual).toEqual(10, tolerance = 10, toleranceType = 'absolute')
~~~~~

Comparing Containers
--------------------

Containers can be compared. Note that dictionary and strings are considered
special cases, and have their own, specialised, comparison methods.

The container comparison has a specialised equality comparison. This is called
in the usual manner:

~~~~~ python
    def test_that_containers_can_be_compared(self):
        actual = (1, 2, 3)
        # We can compare containers
        expect(actual).toEqual((1, 2, 3))
        expect(list(actual)).toEqual([1, 2, 3])
~~~~~

When this fails, the message indicates which elements differ:

~~~~ bash
"Expected [1, 2, 3] to equal [1, 3, 4]. 
First difference is at index 2: 2 != 3"
~~~~ 

This is intended to bring attention to where changes start in large
containers. 

Containers don't have to be exactly the same type. There is some flexibility
over what constitutes 'equivalent' types. For example, tuples and lists can be
compared. This is done by definging two containers with the same contents in the
same order as equal.

~~~~ python
    def test_that_similar_containers_can_be_compared(self):
        actual = (1, 2, 3)
        expect(actual).toEqual([1, 2, 3])
~~~~

Furthermore, containers can be compared to other containers, using toBeASupersetOf and
toBeASubsetOf:

~~~~~ python
    def test_that_set_relations_can_be_expected(self):
        # We can also expect the actual to be a superset or
        # a subset of another container. This generalises
        # the pyhton sets, so that set comparisons can work
        # on lists and tuples:
        actual = (1,2,3) # a tuple
        expect(actual).toBeASupersetOf([2]) 
        expect(actual).toBeASubsetOf([0,1,2,3,4])        
~~~~~

Dictionary comparisons
----------------------

Dictionaries are slightly richer than standard containers, and having their
own comparison assertions allow more descriptive errors to be made.

There is a dictionary-specific equality method.

~~~~~ python
    def test_dictionary_equality(self):
        # Dictionaries can be compared. The failure message
        # then knows it is a dictionary being compared and
        # adds some more useful information to help understand
        # the cause of the failure.
        actual = {"a" : 1,
                  "b" : 2 }

        expect(actual).toEqual({"a":1, "b":2})
~~~~~

If the dictionaries to not match, the error message looks like these:
~~~~~ bash
"Expected {} to be a dictionary containing 1 item"
"Expected {'b': 2, 'a': 1} to equal {'z': 26, 'a': 1}
First missing key is 'b'"
"Expected {'b': 2, 'a': 1} to equal {'b': 26, 'a': 1}
First difference at key 'b': Expected 2 to equal 26"
~~~~

Dictionaries can also be expected to contain specific keys:

~~~~~ python
    def test_dictionary_contains_key(self):
        # Whether a dictionary contains a key is a useful test,
        # and having a method for it can give a more
        # enlightening error message than using a container
        # comparison on the keys view:
        actual = {"a" : 1, 
                  "b" : 2}

        expect(actual).toContainKey("a")
        expect(actual).Not.toContainKey(1)
~~~~~

The messages received from keys missing are more helpful than performing
container expectations on the keys view:

~~~~~ bash
"Expected {'b': 2, 'a': 1} to contain key 'z'"
~~~~~ 

Of course, dictionaries also contain values, so there is also a toContainValue:

~~~~~ python
    def test_dictionary_contains_value(self):
        # Whether a dictionary contains a value is also a useful
        # test, and gives a more enlightening message than using
        # a conainer comparison on the values view.
        actual = {"a" : 1, 
                  "b" : 2}

        expect(actual).toContainValue(1)
        expect(actual).Not.toContainValue("a")
~~~~~

The messages received from values missing are more helpful than performing
container expectations on the values view:

~~~~~ bash
"Expected {'b': 2, 'a': 1} to contain value 26"
~~~~~ 

Comparing strings
-----------------

Strings are compared using a specialised class, which gives richer messages on
string equality comparisons, and adds methods to match substrings at the start,
end end inside the string. It also provides methods to match against regular expression
patterns.

Both strings and multiline strings can be compared:

~~~~~ python
    def test_string_equal(self):
        # Strings can be compared for equality.
        actual = "asdf"
        expect(actual).toEqual("asdf")
        
    def test_multiline_string_equal(self):
        # Multi-line strings can be compared. When they are
        # any differences are reported using the pyhton
        # difflib utility.
        actual = """asdf
lqwerty
poiu
zzzz"""
        expect(actual).toEqual("""asdf
lqwerty
poiu
zzzz""")
~~~~~

When the comparison fails, a diff between the two strings is generated
and added to the exception message:

~~~~ bash
"Expected 'asdf
lqwerty
poiu
zzzz' to equal 'asdfZ
lqwerty
XXXX
zzzz'
Difference is:
- asdf
+ asdfZ
?     +

  lqwerty
- poiu
+ XXXX
  zzzz"
~~~~~

Strings starts and ends can also be compared:

~~~~ python
    def test_string_starts_with(self):
        # Strings can be expected to start with a certain substring
        actual = "asdf"
        expect(actual).toStartWith("as")

    def test_string_ends_with(self):
        # Strings can be expected to end with a certain substring
        actual = "asdf"
        expect(actual).toEndWith("df")
~~~~~

The messages then generated look like:
~~~~~ bash
"Expected 'asdf' to be a string starting with 'df'
Difference is:
- asdf
+ df"
"Expected 'asdf' to be a string ending with 'as'
Difference is:
- asdf
+ as"
~~~~~

String contents can be compared using toContain:

~~~~~ python
    def test_string_to_contain(self):
        # Strings can be expected to contain substrings
        actual = "asdf"
        expect(actual).toContain("sd")
~~~~~

The message on error looks like
~~~~~ bash
"Expected 'asdf' to be a string containing 'ds'"
~~~~~

And strings can be expected to match against regular expression patterns:

~~~~~ python
    def test_string_toMatch(self):
        # String can be expected to match string and compiled
        # regular expression patterns
        actual = "asdf"

        pattern = re.compile(".sd.")
        expect(actual).toMatch("a..f")
        expect(actual).toMatch(pattern)                
~~~~~

When these assertions fail, it leads to messages that look like:

~~~~~ bash
"Expected 'asdf' to be a string matching regular expression pattern '[a-z]+0'"
~~~~~

