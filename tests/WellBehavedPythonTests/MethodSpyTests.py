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

from WellBehavedPython.api import *
from WellBehavedPython.MethodSpy import *

from .Engine.SampleTestCases import *

import io

class MethodSpyTests(TestCase):

    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def targetMethod(self):
        """Method with a manual spy.

        This method is used for testing of andCallThrough."""
        self.targetMethodCalled = True
        return 'targetMethodReturnValue'

    def targetMethodWithPositionalArgs(self, a):
        self.targetMethodCalled = True
        self.targetArgs = a

    def targetMethodWithKeywordArgs(self, first=None):
        self.targetMethodCalled = True
        self.targetArgs = first

    def targetMethodWhichRaisesException(self):
        raise KeyError('raised by target method')

    def before(self):
        self.spy = MethodSpy("anonymous", self.targetMethod)
        self.targetMethodCalled = False

    def test_that_uncalled_spy_hasBeenCalled_returns_False(self):
        # Where
        spy = self.spy

        # When

        # Then
        expect(spy.hasBeenCalled()).toBeFalse()

    def test_that_uncalled_spy_getNumberOfCalls_returns_0(self):
        # Where
        spy = self.spy

        # When

        # Then
        expect(spy.getNumberOfCalls()).toEqual(0)

    def test_that_called_spy_hasBeenCalled_returns_True(self):
        # Where
        spy = self.spy

        # When
        spy()

        # Then
        expect(spy.hasBeenCalled()).withUserMessage(
            "Called spy should claim to have been called").toBeTrue()

    def test_that_spy_called_once_getNumberOfCalls_returns_1(self):
        # Where
        spy = self.spy

        # When
        spy()

        # Then
        expect(spy.getNumberOfCalls()).withUserMessage("Number of calls").toEqual(1)
        
    def test_that_spy_called_twice_getNumberOfCalls_returns_2(self):
        # Where
        spy = self.spy

        # When
        spy()
        spy()

        # Then
        expect(spy.getNumberOfCalls()).withUserMessage("Number of calls").toEqual(2)

    def test_that_spy_description_is_based_on_methodName(self):
        # Where
        anonymousSpy = self.spy
        namedSpy= MethodSpy(methodName = "test_function")

        # Then
        expect(anonymousSpy.getDescription()).toEqual("<anonymous>")
        expect(namedSpy.getDescription()).toEqual("<test_function>")        

    def test_that_ordinary_arguments_can_be_spied_on(self):
        # Where
        spy = self.spy

        # When
        spy(1, "two", [1, 1, 1])

        # Then
        expect(spy.getNumberOfCalls()).toEqual(1)
        expect(spy.hasBeenCalledWith((1,"two", [1, 1, 1]))).toBeTrue()


    def test_that_spy_stores_args_per_invocation(self):
        # Where
        spy = self.spy

        # When
        spy(1)
        spy(2, "two")

        # Then
        expect(spy.getNumberOfCalls()).toEqual(2)
        expectedFirstArguments = (1,)
        expectedSecondArguments = (2, "two")

        expect(spy.hasBeenCalledWith(expectedArgs = expectedFirstArguments, callIndex = 0)).toBeTrue()
        expect(spy.hasBeenCalledWith(expectedSecondArguments, callIndex = 1)).toBeTrue()
        expect(spy.hasBeenCalledWith(expectedSecondArguments, callIndex = 0)).toBeFalse()
        expect(spy.hasBeenCalledWith(expectedSecondArguments, callIndex = None)).toBeTrue()

    def test_that_spy_records_optional_keyword_arguments(self):
        # Where
        spy = self.spy

        # When
        spy(first="the worst", second="the best")
        expectedFirstArguments = {"first":"the worst", "second":"the best"}

        # Then
        expect(spy.hasBeenCalledWith(expectedKeywordArgs = expectedFirstArguments)).toBeTrue()
        expect(spy.hasBeenCalledWith(expectedKeywordArgs = {})).toBeFalse()

    def test_no_arguments_represented_as_parentheses(self):
        # Where
        spy = self.spy

        # When
        string = spy.formatCallArguments()

        # Then
        expect(string).toEqual('()')

    def test_one_argument_represented_with_no_comma(self):
        # Where
        spy = self.spy
        
        # When
        string = spy.formatCallArguments((1,))

        # Then
        expect(string).toEqual('(1)')

    def test_string_argument_wrapped_in_quotes(self):
        # Where
        spy = self.spy
        
        # When
        string = spy.formatCallArguments(('one',))

        # Then
        expect(string).toEqual("('one')")

    def test_formatting_arguments_speartes_them_by_comma_space(self):
        # Where
        spy = self.spy

        # When
        string = spy.formatCallArguments((1, 'two'))

        # Then
        expect(string).toEqual("(1, 'two')")

    def test_formatting_one_keyword_argument(self):
        # Where
        spy = self.spy

        # When
        string = spy.formatCallArguments(None, {'arg': 'value'})

        # Then
        expect(string).toEqual("(arg='value')")

    def test_formatting_two_keyword_arguments(self):
        # Where
        spy = self.spy

        # When
        string = spy.formatCallArguments(None, {'a': 1, 'b': 'two'})

        # Then
        expect(string).toEqual("(a=1, b='two')")
    
    def test_formatting_positional_and_keyword_arguments(self):
        # Where
        spy = self.spy

        # When
        string = spy.formatCallArguments((1,), {'a': 2, 'b':'three'})

        # Then
        expect(string).toEqual("(1, a=2, b='three')")

    def test_call_report_handles_positional_arguments(self):
        # Where
        spy = self.spy

        # When
        spy(1)

        # Then
        expect(spy.generateCallReport()).toEqual("(1)\n")

    def test_call_report_handles_keyword_arguments(self):
        # Where
        spy = self.spy

        # When
        spy(a=1)

        # Then
        expect(spy.generateCallReport()).toEqual("(a=1)\n")        

    def test_call_report_handles_positiona_and_keyword_arguments(self):
        # Where
        spy = self.spy

        # When
        spy(1, a=2)

        # Then
        expect(spy.generateCallReport()).toEqual("(1, a=2)\n")

    def test_call_report_handles_multiple_calls(self):
        # Where
        spy = self.spy

        # When
        spy(1)
        spy(a='1')

        # Then
        expect(spy.generateCallReport()).toEqual("""(1)
(a='1')
""")
    
    def test_that_unconfigured_spy_returns_None(self):
        # Where
        spy = self.spy

        # When
        value = spy()

        # Then
        expect(value).toBeNone()

    def test_that_spy_can_be_configured_to_return_a_set_value(self):
        # Where
        spy = self.spy
        returnValue = 3
        spy.andReturn(returnValue)

        # When
        value = spy()

        # Then
        expect(value).withUserMessage("Spy should return the configured return value of {}".format(
                returnValue)).Not.toBeNone()
        expect(value).toEqual(returnValue)

    def test_that_spy_can_be_configured_to_raise_a_given_exception(self):
        # Where
        spy = self.spy
        spy.andRaise(KeyError)

        #
        expect(lambda: spy()).withUserMessage('spy configured as saboteur should raise the given exception class').toRaise(KeyError)

    def test_that_when_exceptions_and_return_values_combined_exceptions_win(self):
        # Where
        spy = self.spy
        anotherSpy = MethodSpy()

        spy.andReturn(2).andRaise(KeyError)
        anotherSpy.andRaise(KeyError).andReturn(3)
        
        # Then
        expect(spy).toRaise(KeyError)
        expect(anotherSpy).toRaise(KeyError)

    def test_that_targetMethod_sets_called_flag(self):
        # Where
        valueBefore = self.targetMethodCalled

        # When
        self.targetMethod()
        valueAfter = self.targetMethodCalled

        # Then
        expect(valueBefore).withUserMessage('called flag should be false by default').toBeFalse()
        expect(valueAfter).withUserMessage('called flag should be true after call').toBeTrue()

    def test_that_targetMethodWithPoisitionalArgs_sets_called_flag(self):
        # Where
        valueBefore = self.targetMethodCalled

        # When
        self.targetMethodWithPositionalArgs(1)
        valueAfter = self.targetMethodCalled

        # Then
        expect(valueBefore).withUserMessage('called flag should be false by default').toBeFalse()
        expect(valueAfter).withUserMessage('called flag should be true after call').toBeTrue()
        expect(self.targetArgs).toEqual(1)

    def test_that_targetMethodWithKeywordArgs_sets_called_flag(self):
        # Where
        valueBefore = self.targetMethodCalled

        # When
        self.targetMethodWithKeywordArgs(first='the worst')
        valueAfter = self.targetMethodCalled

        # Then
        expect(valueBefore).withUserMessage('called flag should be false by default').toBeFalse()
        expect(valueAfter).withUserMessage('called flag should be true after call').toBeTrue()
        expect(self.targetArgs).toEqual('the worst')
        

    def test_that_spy_with_call_through_set_calls_original_method(self):
        # Where
        spy = self.spy
        spy.andCallThrough()

        # When
        spy()

        # Then
        expect(self.targetMethodCalled).toBeTrue()

    def test_that_spy_with_call_through_set_passes_positional_args_to_original_method(self):
        # Where
        spy = MethodSpy("targetMethodWithPositionalArgs", self.targetMethodWithPositionalArgs)
        spy.andCallThrough()

        # When
        spy(1)

        # Then
        expect(self.targetMethodCalled).toBeTrue()
        expect(self.targetArgs).toEqual(1)

    def test_that_spy_with_call_through_set_passes_keyword_args_to_original_method(self):
        # Where
        spy = MethodSpy('targetMethodWithKeywordArgs', self.targetMethodWithKeywordArgs)
        spy.andCallThrough()

        # When
        spy(first = 'the worst')
       
        # Then
        expect(self.targetMethodCalled).toBeTrue()
        expect(self.targetArgs).toEqual('the worst')
 
    def test_that_spy_with_call_through_set_returns_method_value(self):
        # Where
        spy = self.spy
        spy.andCallThrough()

        # When
        value = spy()

        # Then
        expectedValue = self.targetMethod()
        expect(value).Not.toBeNone()
        expect(value).toEqual(expectedValue)

    def test_that_call_through_exception_bubbles_to_test(self):
        # Where
        spy = MethodSpy('targetMethodWhichRaisesException', self.targetMethodWhichRaisesException)
        spy.andCallThrough()

        # Then
        expect(spy).toRaise(KeyError, expectedMessageMatches = 'raised by target method')

    def test_that_return_value_beats_call_through_return_value(self):
        # Where
        overridenReturnValue = 'overriden return value'
        spy1 = MethodSpy('targetMethod', self.targetMethod)
        spy1.andCallThrough().andReturn(overridenReturnValue)

        spy2 = MethodSpy('targetMethod', self.targetMethod)
        spy2.andReturn(overridenReturnValue)

        # When
        actualValue1 = spy1()
        actualValue2 = spy2()

        # Then
        expect(actualValue1).toEqual(overridenReturnValue)
        expect(actualValue2).toEqual(overridenReturnValue)

    def test_that_call_through_exception_beats_andRaise_exception(self):
        # Where
        spy = MethodSpy('targetMethodWhichRaisesException', self.targetMethodWhichRaisesException)
        spy.andCallThrough().andRaise(IOError)

        # Then
        expect(spy).toRaise(KeyError)        

    def test_that_spy_andCall_calls_method_provided(self):
        # Where
        self.lambdaCalled = False
        expectedReturnValue = 'inner method'

        def innerMethod():
            self.lambdaCalled = True
            return expectedReturnValue

        spy = self.spy
        spy.andCall(innerMethod)

        
        # When
        actualReturnValue = spy()

        # Then
        expect(self.lambdaCalled).toBeTrue()
        expect(actualReturnValue).toEqual(expectedReturnValue)
