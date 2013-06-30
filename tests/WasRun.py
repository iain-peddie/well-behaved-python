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
        self.wasTargetMethodCalled = True

    def test_run_template(self):
        self.targetMethod()
        
        assert self.wasBeforeCalled
        assert self.wasTargetMethodCalled        
        
if __name__ == "__main__":
    import os
    import os.path
    import sys

    cwd = os.curdir
    srcPath = os.path.join(cwd, '../src/')
    srcPath = os.path.abspath(srcPath)
    sys.path.append(srcPath)    
    from WellBehavedPython.TestCommand import *

    WasRun("test_run_template").run()

