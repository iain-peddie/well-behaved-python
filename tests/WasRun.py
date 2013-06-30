#!/usr/bin/env python3

class WasRun:

    def __init__(self, testFunctionName):
        self.testMethod = getattr(self, testFunctionName)

    def before(self):
        self.wasBeforeCalled = True

    def run(self):
        """Command to organise a single test run of a single
           test function."""

        self.before()
        self.testMethod()

    def targetMethod(self):
        """Target method when running unit tests."""
        self.wasRun = True

    def test_TestCommand_runsTest(self):
        self.targetMethod()
        assert self.wasRun

    def test_before_run(self):
        self.targetMethod()
        assert self.wasBeforeCalled
        
if __name__ == "__main__":
    import os
    import os.path
    import sys

    cwd = os.curdir
    srcPath = os.path.join(cwd, '../src/')
    srcPath = os.path.abspath(srcPath)
    sys.path.append(srcPath)    
    from WellBehavedPython.TestCommand import *



    WasRun("test_TestCommand_runsTest").run()
    WasRun("test_before_run").run()

