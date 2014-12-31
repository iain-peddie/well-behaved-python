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

from .ArrayExpectations import ArrayExpectations

from numpy.dual import det

class SquareMatrixExpectations(ArrayExpectations):

    def toBeInvertible(self):
        """Indicates that actual is expected to be invertible.

        The logic for this is:
          - actual should be square (implicit)
          - actual should have a non-zero determinant.

        The zero determinant property is used as it is faster to
        calculate than calculating the full inverse, as it should
        only involve perfoming an UL factorization."""

        # no call to compare types needed, as no 'expected' value is
        # given

        metric = det(self.actual)

        message = self.buildMessage("to be invertible", None)

        if metric < self.zeroTolerance:
            self.fail(message)
        else:
            self.success(message)

    
