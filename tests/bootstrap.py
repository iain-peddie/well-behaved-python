#!/usr/bin/env python3

import sys
import os
import os.path


def main():
    setup()
    from WasRun import WasRun

    # test block
    test = WasRun("test_TestCommand_runsTest")
    test.run()
    test = WasRun("test_before_run")
    test.run()

if __name__ == "__main__":
    main()
