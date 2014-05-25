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

from .MethodSpy import MethodSpy

class ObjectSpy:
    """A class for creating full spy objects with many method spies."""

    def __init__(self, methods = (), properties = ()):
        """Constructor.

        Inputs
        ------
        methods: Iterable container containing the names of the methods 
                 that the object should have.
        properites: Iterable container containing the names of the properties
                    that the object should have."""

        for methodName in methods:
            setattr(self, methodName, MethodSpy(methodName))
        for propertyName in properties:
            setattr(self, propertyName, None)
