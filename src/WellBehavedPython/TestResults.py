#!/usr/bin/env python3

# Copyright 2013 Iain Peddie inr314159@hotmail.com
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

class TestResults:

    def __init__(self):
        self.testCount = 0
        self.failCount = 0

    def registerTestStarted(self):
        self.testCount += 1

    def registerTestFailed(self):
        self.failCount += 1
    
    def summary(self):
        if self.testCount > 1:
            plural = "s"
        else:
            plural = ""
        return "{} failed from {} test{}".format(
            self.failCount, self.testCount, plural)
