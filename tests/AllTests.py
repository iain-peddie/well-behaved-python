#!/usr/bin/env python3

# Copyright 2013-4 Iain Peddie inr314159@hotmail.com
# 
#    This file is part of WellBehavedPython
#
#    WellBehavedPython is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WellBehavedPython is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WellBehavedPython. If not, see <http://www.gnu.org/licenses/>.

import sys

from WellBehavedPython.api import discoverTests
from WellBehavedPython.Runners.ConsoleTestRunner import ConsoleTestRunner
from WellBehavedPython.Runners.VerboseConsoleTestRunner import VerboseConsoleTestRunner



def main():
    try:
        suite = discoverTests('WellBehavedPythonTests', ignoreFilters = ['Samples'])
        
        buffer = True

        if len(sys.argv) > 1 and sys.argv[1] == '--verbose':
            runner = VerboseConsoleTestRunner(bufferOutput = buffer)
        else:
            runner = ConsoleTestRunner(bufferOutput = buffer)
        results = runner.run(suite)

        sys.__stdout__.flush()
        sys.__stderr__.flush()

        exit(results.countFailures() + results.countErrors() > 0)
    except Exception as ex:        
    
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        traceback.print_exc(file = sys.stdout)
            
if __name__ == "__main__":
    main()

