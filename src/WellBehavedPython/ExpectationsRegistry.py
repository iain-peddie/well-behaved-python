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

class ExpectationsFactory:
    """Class responsible for creating and configureing an Expectations object.

    The ExpectationsRegistry will use a collection of these to decide which
    expectations object to create for each item."""

    def __init__(self, createPredicate, createExpectations):
        """Constructor

        Inputs
        ------
        createPredicate: callable item which returns True or False
                         depending on whether it's argument is appropriate
                         for the type of ExpectationsObject this factory
                         is configured to create
        createExpectations: callable object that is used to create
                            an expectations object in isolation."""

        self.createPredicate = createPredicate
        self.createExpectations = createExpectations

    def shouldCreateFor(self, item):

        return self.createPredicate(item)

class ExpectationsRegistry:
    pass


