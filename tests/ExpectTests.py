#!/usr/bin/env python3

# Copyright 2013 Iain Peddie inr314159@hotmail.com
# 
#    This file is part of WellBehavedPython
#
#    WellBehavedPython is free softwaree: you can redistribute it and/or modify
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

from WellBehavedPython.TestCase import *
from WellBehavedPython.TestSuite import *
from WellBehavedPython.Expect import *

class ExpectTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)
    
    @staticmethod
    def suite():
        testMethods = [
            "test_expects_fail_throws_AssertionError",
            "test_failure_stores_message_if_provided",
            ]
        
        suite = TestSuite()
    
        for testMethod in testMethods:
            suite.add(ExpectTests(testMethod))
        return suite

    def test_expects_fail_throws_AssertionError(self):
        # This would be easier if there was an expected exception,
        # but that comes later
        flag = True
        try:
            Expect(True).fail()
            flag = False
        except AssertionError:
            pass
        
        assert(flag)

    def test_failure_stores_message_if_provided(self):
        flag = True
        try:
            Expect(True).fail("ExpectedMessage")
            flag = False
        except AssertionError as ex:
            assert ex.args[0] == "ExpectedMessage"
        
        assert flag, "expected message not stored in exception"

if __name__ == "__main__":
    suite = ExpectTests.suite()
    results = TestResults()
    suite.run(results)
    
    print(results.summary())

