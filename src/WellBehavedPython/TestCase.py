#!/usr/bin/env python3

class TestCase:
    
    def __init__(self, testMethodName):
        """Creates an instance of this test class configured
        to run the method testMethodName in the actual test object."""
        self.testMethod = getattr(self, testMethodName)

    def before(self):
        """Override this to create your before tests setup logic"""
        pass

    def run(self):
        """Command to organise a single test run of a single
           test function."""

        self.before()
        self.testMethod()


