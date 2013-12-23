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

from WellBehavedPython.TestCase import *
from WellBehavedPython.MethodSpy import MethodSpy
from WellBehavedPython.api import *
from WellBehavedPython.MethodSpyExpectations import MethodSpyExpectations
from WellBehavedPython.BaseExpect import BaseExpect

class MethodSpyExpectationsTestsBase(TestCase):
    def __init__(self, name):
        TestCase.__init__(self, name)

    def createMethodSpyWhichHasNotBeenCalled(self):
        spy = MethodSpy()
        return spy

    def createMethodSpyWhichHasBeenCalled(self):
        spy = self.createMethodSpyWhichHasNotBeenCalled()
        self.call(spy)
        return spy

    def call(self, spy):
        spy()


class MethodSpyExpectationsTests(MethodSpyExpectationsTestsBase):
    def __init__(self, name):
        MethodSpyExpectationsTestsBase.__init__(self, name)

    def test_spy_expectations_registered_for_spies_by_default(self):
        # Where
        spy = MethodSpy()
        
        # When
        expecter = expect(spy)

        # Then
        expect(expecter).toBeAnInstanceOf(MethodSpyExpectations)
        expect(expecter).toBeAnInstanceOf(BaseExpect)

    def test_expect_method_called_passes_when_method_has_been_called(self):
        # Where
        calledSpy = self.createMethodSpyWhichHasBeenCalled()

        # Then
        expect(calledSpy).toHaveBeenCalled()

    def test_expect_method_called_fails_when_method_has_not_been_called(self):
        # Where
        uncalledSpy = self.createMethodSpyWhichHasNotBeenCalled()
        
        # Then
        expect(lambda: expect(uncalledSpy).toHaveBeenCalled()).toRaise(
            AssertionError, 
            expectedMessage = 'Expected <anonymous> to have been called')

    def test_expect_method_called_twice_passes_when_method_has_been_called_twice(self):
        # Where
        calledSpy = self.createMethodSpyWhichHasBeenCalled()
        self.call(calledSpy)

        # Then
        expect(calledSpy).toHaveBeenCalled(times = 2)

    def test_expect_method_called_twice_failed_if_spy_only_called_once(self):
        # Where
        calledSpy = self.createMethodSpyWhichHasBeenCalled()

        # Then
        expect(lambda: expect(calledSpy).toHaveBeenCalled(times = 2)).toRaise(
            AssertionError,
            expectedMessage = 'Expected <anonymous> to have been called 2 times')

    def test_expect_method_called_twice_failed_if_spy_only_called_three_times(self):
        # Where
        calledSpy = self.createMethodSpyWhichHasBeenCalled()
        self.call(calledSpy)
        self.call(calledSpy)

        # Then
        expect(lambda: expect(calledSpy).toHaveBeenCalled(times = 2)).toRaise(
            AssertionError,
            expectedMessage = 'Expected <anonymous> to have been called 2 times')

    def test_expect_toHaveBeenCalled_with_usermessage(self):
        # Where
        uncalledSpy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        # do nothing

        # Then
        expect(lambda:
                   expect(uncalledSpy).withUserMessage("userMessage").toHaveBeenCalled()).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage:")

    def test_expect_toHaveBeenCalled_1_times_message(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()
        
        # When

        # Then
        expect(lambda:
                   expect(spy).toHaveBeenCalled(times = 1)).toRaise(
            AssertionError, 
            expectedMessage = "Expected <anonymous> to have been called 1 time")

    def test_expect_called_with_passes_when_matching_one_call_exactly(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(1)

        # Then
        expect(spy).toHaveBeenCalledWith(1) # not to raise

    def test_expect_method_called_with_fails_when_spy_never_called(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When

        # Then
        expect(
            lambda: expect(spy).toHaveBeenCalledWith(2)).toRaise(
            AssertionError,
            expectedMessage = "Expected <anonymous> to have been called with (2), but it was not called")

    def test_expect_method_called_with_fails_when_positional_args_dont_match_one_call(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()
        
        # When
        spy(1, "two")

        # Then
        expect(
            lambda: expect(spy).toHaveBeenCalledWith(3, "four")).toRaise(
            AssertionError, 
            expectedMessage = """Expected <anonymous> to have been called with (3, 'four'), but it was called 1 time with:
(1, 'two')
""")

    def test_expect_method_called_passes_when_method_matches_one_of_many_calls(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()
        
        # When
        spy(1, "two")
        spy(5, "six")

        # Then
        expect(
            lambda: expect(spy).toHaveBeenCalledWith(3, "four")).toRaise(
            AssertionError, 
            expectedMessage = """Expected <anonymous> to have been called with (3, 'four'), but it was called 2 times with:
(1, 'two')
(5, 'six')
""")

    def test_expect_method_called_with_keyword_passes_when_called_with_keywords(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(a=1)
        
        # Then
        expect(spy).toHaveBeenCalledWith(a=1)

    def test_expect_method_called_with_keywords_fails_when_never_called(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # Then
        expect(
            lambda: expect(spy).toHaveBeenCalledWith(a=1)).toRaise(
            AssertionError, 
            expectedMessage = "Expected <anonymous> to have been called with (a=1), but it was not called")

    def test_expect_method_called_with_keywords_fails_when_no_call_matches_keywords(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(b=2)

        # Then
        expect(
            lambda: expect(spy).toHaveBeenCalledWith(a=1)).toRaise(
            AssertionError, 
            expectedMessage = """Expected <anonymous> to have been called with (a=1), but it was called 1 time with:
(b=2)
""")

    def test_expect_method_called_with_keywords_fails_if_keywords_match_and_values_dont(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(a=2)

        # Then
        expect(
            lambda: expect(spy).toHaveBeenCalledWith(a=1)).toRaise(
            AssertionError, 
            expectedMessage = """Expected <anonymous> to have been called with (a=1), but it was called 1 time with:
(a=2)
""")

    def test_expect_called_with_passes_when_matching_one_mixed_args_call(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(1, a=2)

        # Then
        expect(spy).toHaveBeenCalledWith(1, a=2)

    def test_expect_called_with_fails_with_mismatching_mixed_args_call(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(3, b=4)

        # Then
        expect(
            lambda: expect(spy).toHaveBeenCalledWith(1, a=2)).toRaise(
            AssertionError,
            expectedMessage = """Expected <anonymous> to have been called with (1, a=2), but it was called 1 time with:
(3, b=4)
""")

    def test_expect_called_with_userMessage_when_no_calls(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # Then
        expect(
            lambda: expect(spy).withOptions(userMessage = "userMessage").toHaveBeenCalledWith(1, a=2)).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

    def test_expect_called_with_userMessage_when_no_calls(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(3, b=4)

        # Then
        expect(
            lambda: expect(spy).withUserMessage("userMessage").toHaveBeenCalledWith(1, a=2)).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

    def test_expect_called_at_index_with_only_looks_at_indexth_call(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()
        spy(1, a=2)
        spy(3, b=4)
        spy(5, c=6)
        spy(7, d=8)

        expect(
            lambda: expect(spy).forCallNumber(1).toHaveBeenCalledWith(3, b=4)).toRaise(
            AssertionError,
            expectedMessage = """Expected <anonymous> to have been called with (3, b=4) on the 1st call, but it was called with:
=> (1, a=2)
(3, b=4)
(5, c=6)
(7, d=8)
""")        

        expect(
            lambda: expect(spy).forCallNumber(2).toHaveBeenCalledWith(1, a=2)).toRaise(
            AssertionError,
            expectedMessage = """Expected <anonymous> to have been called with (1, a=2) on the 2nd call, but it was called with:
(1, a=2)
=> (3, b=4)
(5, c=6)
(7, d=8)
""")

        expect(
            lambda: expect(spy).forCallNumber(3).toHaveBeenCalledWith(1, a=2)).toRaise(
            AssertionError,
            expectedMessage = """Expected <anonymous> to have been called with (1, a=2) on the 3rd call, but it was called with:
(1, a=2)
(3, b=4)
=> (5, c=6)
(7, d=8)
""")

        expect(
            lambda: expect(spy).forCallNumber(4).toHaveBeenCalledWith(1, a=2)).toRaise(
            AssertionError,
            expectedMessage = """Expected <anonymous> to have been called with (1, a=2) on the 4th call, but it was called with:
(1, a=2)
(3, b=4)
(5, c=6)
=> (7, d=8)
""")

    def test_expect_method_called_at_least_one_time_passes_if_called_once(self):
        # Where
        spy = self.createMethodSpyWhichHasBeenCalled()

        # Then
        expect(spy).toHaveBeenCalledAtLeast(1).time()

    def test_expect_method_Called_at_least_once_passes_if_called_twice(self):
        # Where
        spy = self.createMethodSpyWhichHasBeenCalled()
        spy() # second call

        # Then
        expect(spy).toHaveBeenCalledAtLeast(1).time()

    def test_expect_method_called_at_least_one_time_fails_if_never_called(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # Then
        expect(
            lambda: expect(spy).toHaveBeenCalledAtLeast(1).time()).toRaise(
            AssertionError,
            expectedMessage = "Expected <anonymous> to have been called at least 1 time, but it was never called.")

    def test_expect_method_called_at_least_two_times_fails_with_only_one_call(self):
        # Where
        spy = self.createMethodSpyWhichHasBeenCalled()

        # Then
        expect(
            lambda: expect(spy).toHaveBeenCalledAtLeast(2).times()).toRaise(
        AssertionError,
        expectedMessage = "Expected <anonymous> to have been called at least 2 times, but it was called 1 time.")

    def test_expect_method_called_at_most_one_time_passes_if_never_called(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        expect(spy).toHaveBeenCalledAtMost(1).time()

    def test_expect_method_called_at_most_one_time_passes_if_called_once(self):
        # Where
        spy = self.createMethodSpyWhichHasBeenCalled()

        # When
        expect(spy).toHaveBeenCalledAtMost(1).time()
            

class MethodSpyNotExpectationsTests(MethodSpyExpectationsTestsBase):

    def __init__(self, name):
        MethodSpyExpectationsTestsBase.__init__(self, name)

    def test_expect_method_not_called_fails_when_method_has_been_called(self):
        # Where
        calledSpy = self.createMethodSpyWhichHasBeenCalled()

        # Then
        expect(lambda: expect(calledSpy).Not.toHaveBeenCalled()).toRaise(
            AssertionError, 
            expectedMessage = 'Expected <anonymous> not to have been called')

    def test_expect_method_not_called_n_times_fails_when_called_n_times(self):
        # Where
        calledSpy = self.createMethodSpyWhichHasBeenCalled()
        calledSpy()

        # Then
        expect(lambda: expect(calledSpy).Not.toHaveBeenCalled(times = 2)).toRaise(
            AssertionError, 
            expectedMessage = 'Expected <anonymous> not to have been called 2 times')
            

    def test_expect_method_not_called_passes_when_method_has_not_been_called(self):
        # Where
        uncalledSpy = self.createMethodSpyWhichHasNotBeenCalled()
        
        # Then
        expect(uncalledSpy).Not.toHaveBeenCalled()

    def test_expect_method_not_called_with_passes_when_message_not_called(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # Then
        expect(spy).Not.toHaveBeenCalledWith(1)

    def test_expect_method_not_called_with_passes_when_positional_args_mismatch(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(1, "two")

        # Then
        expect(spy).Not.toHaveBeenCalledWith(3, "four")

    def test_expect_method_not_called_with_1two_fails_when_spy_called_with_1two(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(1, "two")

        # Then
        expect(
            lambda: expect(spy).Not.toHaveBeenCalledWith(1, 'two')).toRaise(
            AssertionError,
            expectedMessage = """Expected <anonymous> not to have been called with (1, 'two'), but it was called 1 time with:
(1, 'two')
""")

    def test_expect_method_not_called_with_keywords_passes_when_method_not_called(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # Then
        expect(spy).Not.toHaveBeenCalledWith(a=1)

    def test_expect_method_not_called_with_keywords_passes_when_keywords_mismatch(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(b=2)

        # Then
        expect(spy).Not.toHaveBeenCalledWith(a=1)

    def test_expect_method_not_called_with_keyowrds_passes_when_keywords_match_but_values_dont(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(a=2)

        # Then
        expect(spy).Not.toHaveBeenCalledWith(a=1)

    def test_expect_method_not_called_with_keywords_fails_when_keywords_and_values_match(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(a=1)

        # Then
        expect(
            lambda: expect(spy).Not.toHaveBeenCalledWith(a=1)).toRaise(
            AssertionError,
            expectedMessage = """Expected <anonymous> not to have been called with (a=1), but it was called 1 time with:
(a=1)
""")

    def test_expect_method_not_called_with_mix_of_args_passes_when_not_called(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # Then
        expect(spy).Not.toHaveBeenCalledWith(1, a=2)

    def test_expect_method_not_called_with_mix_of_args_passes_when_positional_args_mismatch(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(3, a=2)

        # Then
        expect(spy).Not.toHaveBeenCalledWith(1, a=2)

    def test_expect_method_not_called_with_mix_of_args_passes_when_keyword_args_mismatch(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(1, a=3)

        # Then
        expect(spy).Not.toHaveBeenCalledWith(1, a=2)

    def test_expect_method_not_called_with_mix_of_args_fails_when_all_args_match(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()

        # When
        spy(1, a=2)

        # Then
        expect(
            lambda: expect(spy).Not.toHaveBeenCalledWith(1, a=2)).toRaise(
            AssertionError, 
            expectedMessage = """Expected <anonymous> not to have been called with (1, a=2), but it was called 1 time with:
(1, a=2)
""")
        
    def test_expect_not_calledWith_prepends_userMessage(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()
        spy(1, a=2)

        # Then
        expect(
            lambda: expect(spy).withUserMessage("userMessage").Not.toHaveBeenCalledWith(1, a=2)).toRaise(
            AssertionError,
            expectedMessageMatches="^userMessage")
        
        
    def test_expect_not_called_at_index_with_only_looks_at_indexth_call(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()
        spy(1, a=2)
        spy(3, b=4)
        spy(5, c=6)
        spy(7, d=8)

        expect(
            lambda: expect(spy).forCallNumber(1).Not.toHaveBeenCalledWith(1, a=2)).toRaise(
            AssertionError,
            expectedMessage = """Expected <anonymous> not to have been called with (1, a=2) on the 1st call, but it was called with:
=> (1, a=2)
(3, b=4)
(5, c=6)
(7, d=8)
""")        

        expect(
            lambda: expect(spy).forCallNumber(2).Not.toHaveBeenCalledWith(3, b=4)).toRaise(
            AssertionError,
            expectedMessage = """Expected <anonymous> not to have been called with (3, b=4) on the 2nd call, but it was called with:
(1, a=2)
=> (3, b=4)
(5, c=6)
(7, d=8)
""")

        expect(
            lambda: expect(spy).forCallNumber(3).Not.toHaveBeenCalledWith(5, c=6)).toRaise(
            AssertionError,
            expectedMessage = """Expected <anonymous> not to have been called with (5, c=6) on the 3rd call, but it was called with:
(1, a=2)
(3, b=4)
=> (5, c=6)
(7, d=8)
""")

        expect(
            lambda: expect(spy).forCallNumber(4).Not.toHaveBeenCalledWith(7, d=8)).toRaise(
            AssertionError,
            expectedMessage = """Expected <anonymous> not to have been called with (7, d=8) on the 4th call, but it was called with:
(1, a=2)
(3, b=4)
(5, c=6)
=> (7, d=8)
""")

    def test_expect_method_not_called_at_least_one_time_passes_if_never_called(self):
        # Where
        spy = self.createMethodSpyWhichHasNotBeenCalled()
        
        # When
        expect(spy).Not.toHaveBeenCalledAtLeast(1).time()

    def test_expect_method_not_called_at_least_one_time_fails_if_called_once(self):
        # Where
        spy = self.createMethodSpyWhichHasBeenCalled()

        # Then
        expect(
            lambda: expect(spy).Not.toHaveBeenCalledAtLeast(1).time()).toRaise(
            AssertionError,
            expectedMessage = "Expected <anonymous> not to have been called at least 1 time, but it was called 1 time.")

    def test_expect_method_not_called_at_least_two_times_fails_if_called_twice(self):
        # Where
        spy = self.createMethodSpyWhichHasBeenCalled()
        spy() # second call

        # Then
        expect(
            lambda: expect(spy).Not.toHaveBeenCalledAtLeast(1).time()).toRaise(
            AssertionError,
            expectedMessage = "Expected <anonymous> not to have been called at least 1 time, but it was called 2 times.")
        
