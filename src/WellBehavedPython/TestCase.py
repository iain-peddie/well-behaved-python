#!/usr/bin/env python3

class TestCase:
    
    def __init__(self, testMethodName):
        """Creates an instance of this test class configured
        to run the method testMethodName in the actual test object."""
        self.testMethod = getattr(self, testMethodName)

    def before(self):
        """Override this to create the setup logic which should run
        before each individual test method."""

    def after(self):
        """Override this to create the cleanup logic which should run
        after each individual test method."""

    def run(self):
        """Command to organise a single test run of a single
           test function."""

        self.before()
        try:
            self.testMethod()
        except:
            self.after()


