#!/usr/bin/env python3

import sys
import os
import os.path


def main():
    setup()
    from WasRun import WasRun
    test = WasRun("test_TestCommand_runsTest")
    test.run()

def setup():
    cwd = os.curdir
    srcPath = os.path.join(cwd, '../src/')
    srcPath = os.path.abspath(srcPath)
    sys.path.append(srcPath)    

if __name__ == "__main__":
    setup()
    main()
