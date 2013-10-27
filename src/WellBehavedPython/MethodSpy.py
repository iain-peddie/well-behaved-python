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

class MethodSpy:

    def __init__(self, methodName = "anonymous"):
        self.methodName = methodName
        self.callCount = 0

    def __call__(self):
        self.callCount += 1

    def getDescription(self):
        return "<{}>".format(self.methodName)

    def getNumberOfCalls(self):
        return self.callCount

    def hasBeenCalled(self):
        return self.callCount > 0

