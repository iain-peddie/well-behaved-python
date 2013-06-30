#!/usr/bin/env python3

import sys
import os
import os.path

from WasRun import WasRun

def main():
    setup()
#    test_whether_test_is_run() ignoring while working on subtest
    test_TestCommand_runsTest()

def setup():
    cwd = os.curdir
    srcPath = os.path.join(cwd, '../src/')
    srcPath = os.path.abspath(srcPath)
    sys.path.append(srcPath)

def test_TestCommand_runsTest():
    tester = WasRun()
    test = TestCommand(tester.testMethod)
    test.run()
    assert tester.wasRun

def test_whether_test_is_run():
    tester = WasRun()
    test = it("is a test", tester.testMethod)
    test.run()
    assert tester.WasRun

if __name__ == "__main__":
    setup()
    from WellBehavedPython.it import it
    from WellBehavedPython.TestCommand import *
    main()
