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
from WellBehavedPython.api import *

def raise_error():
    raise KeyError("The wrong key was presented")

class DefaultExpectationsTests(TestCase):
    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def test_expects_fail_throws_AssertionError(self):
        # DON'T USE EXPECTED EXCEPTION
        # The test for fail is so fundamental, that it has to be
        # performed with tests outside the framework itself
        # 
        # Otherwise, we're assuming fail works while testing the
        # exceptino based behavior of fail. The test for the 
        # expected message is different, as that is testing the
        # message structure, and not the fundamental pass/fail
        # behavior.
        raised = True
        try:
            expect(True).fail()
            raised = False
        except AssertionError:
            pass
        
        # Fail is so fundamental that we don't bootstrap
        # the asertion with Expect.toBeTrue() as that uses fail
        assert raised, "Expected an AssertionError to have been thrown"    

    def test_failure_stores_message_if_provided(self):
        expect(lambda: expect(True).fail("ExpectedMessage")).toRaise(
            AssertionError,
            expectedMessage = "ExpectedMessage")

    def test_expect_truthy_values_to_be_true_succeeds(self):
        expect(True).toBeTrue()
        expect(1).toBeTrue()
        expect((1)).toBeTrue()

    def test_expect_falsy_values_to_be_true_fails(self):
        values = (False, 0, ())
        expectedMessages = ("Expected False to be True", 
                            "Expected 0 to be True",
                            "Expected () to be True")
        for i in range(0, len(values) - 1):
            expect(lambda: expect(values[i]).toBeTrue()).toRaise(
                AssertionError,
                expectedMessage = expectedMessages[i])

    def test_expect_truthy_values_to_be_false_fails(self):
        values = (True, 1, (1))
        expectedMessages = ("Expected True to be False",
                            "Expected 1 to be False",
                            "Expected (1) to be False")

        for i in range(0, len(values) - 1):
            expect(lambda: expect(values[i]).toBeFalse()).toRaise(
                AssertionError,
                expectedMessage = expectedMessages[i])

    def test_expect_falsy_values_to_be_false_succeeds(self):
        values = (False, 0, ())
        for value in values:
            expect(value).toBeFalse()

    def test_expect_true_prepends_usermessage_to_assertion(self):
        expect(lambda: expect(False).withUserMessage(
                "userMessage").toBeTrue()).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

    def test_expect_false_prepends_usermessage_to_assertion(self):
        expect(lambda: expect(True).withUserMessage("userMessage").toBeFalse()).toRaise(
            AssertionError,
            expectedMessageMatches = "^userMessage")

    def test_expecting_None_toBeNone_passes(self):
        expect(None).toBeNone()

    def test_expecting_False_toBeNone_fails(self):
        expect(lambda: expect(False).toBeNone()).toRaise(
            AssertionError,
            expectedMessage = "Expected False to be None")

    def test_expect_toBeNone_prepends_user_message(self):
        expect(lambda: expect(False).toBeNone("user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_1_instanceof_int_passes(self):
        expect(1).toBeAnInstanceOf(int)

    def test_1_instanceof_float_fails(self):
        expect(lambda: expect(1).toBeAnInstanceOf(float)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 to be an instance of <class 'float'> but was an instance of <class 'int'>")

    def test_instance_of_userclass_passes(self):
        expect(TestResults()).toBeAnInstanceOf(TestResults)

    def test_instance_of_wrong_userclass_fails(self):
        expect(lambda: expect(TestResults()).toBeAnInstanceOf(TestSuite)).toRaise(
            AssertionError,
            expectedMessageMatches = " to be an instance of <class 'WellBehavedPython.TestSuite.TestSuite'>"
            " but was an instance of <class 'WellBehavedPython.TestResults.TestResults'>")

    def test_instance_of_derived_class_matches_base_class(self):
        expect(self).toBeAnInstanceOf(TestCase)

    def test_instance_of_prepends_usermessage(self):
        expect(lambda: 
               expect(1).toBeAnInstanceOf(float, "user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expected_exception_passes_when_exception_matches(self):
        expect(raise_error).toRaise(KeyError)

    def test_expected_exception_passes_when_exception_is_derived_from_match(self):
        expect(raise_error).toRaise(LookupError)
        

    def test_expected_exception_fails_if_exception_not_raised(self):
        # We have to use a manual expected exception here to check that
        # expected exception raises the right exception
        message = ""
        try:
            expect(lambda: None).toRaise(Exception)
        except AssertionError as ex:
            message = ex.args[0]
        butNoneWas = ", but none was"
        expect(message[-len(butNoneWas):]).toEqual(butNoneWas)    

    def test_expected_exception_fails_if_wrong_exception_raised(self):
        message = ""
        try:
            expect(raise_error).toRaise(FloatingPointError)
        except AssertionError as ex:
            message = ex.args[0]
        expect(message).toEqual("Expected <function raise_error> "
                                "to raise an instance of <class 'FloatingPointError'>, "
                                "but it raised an instance of <class 'KeyError'>")

    def test_expected_exception_prepends_usermessage_on_wrong_exception(self):
        message = ""
        try:
            expect(raise_error).toRaise(FloatingPointError, "user message")
        except AssertionError as ex:
            message = ex.args[0]
        expect(message).toEqual("user message: "
                                "Expected <function raise_error> "
                                "to raise an instance of <class 'FloatingPointError'>, "
                                "but it raised an instance of <class 'KeyError'>")

    def test_expected_exception_prepends_usermessage_on_no_exception(self):
        message = ""
        userMessage = "user message"
        try:
            expect(lambda: None).toRaise(KeyError, userMessage)
        except AssertionError as ex:
            message = ex.args[0]
        expect(len(message)).toBeGreaterThan(len(userMessage))
        expect(message[0:len(userMessage) + 2]).toEqual("user message: ")

    def test_expect_exception_with_expected_message_passes(self):
        expect(raise_error).toRaise(
            KeyError,
            expectedMessage = "The wrong key was presented")

    def test_expect_exception_with_unexpected_message_fails(self):
        message = ""
        try:
            expect(raise_error).toRaise(KeyError, expectedMessage = "This is not the right message")
        except AssertionError as ex:
            message = ex.args[0]
        
        expect(message).toEqual("Expected <function raise_error>"
                                " to raise an instance of <class 'KeyError'>"
                                " with message 'This is not the right message'"
                                ", but it raised an instance of <class 'KeyError'>"
                                " with message 'The wrong key was presented'")

    def test_expected_exception_with_message_matching_regexp_passes(self):
        expect(raise_error).toRaise(KeyError, expectedMessageMatches = ".*")

    def test_expected_exception_with_message_not_matching_regexp_fails(self):
        message = ""
        try:
            expect(raise_error).toRaise(
                KeyError,
                expectedMessageMatches = "^not")
        except AssertionError as ex:
            message = ex.args[0]
            
        expect(message).toEqual("Expected <function raise_error>"
                                " to raise an instance of <class 'KeyError'>"
                                " with message matching regular expression '^not'"
                                ", but it raised an instance of <class 'KeyError'>"
                                " with message 'The wrong key was presented'")

    def test_expected_exception_with_message_matching_compiled_regexp_passes(self):
        regexp = re.compile(".*")
        expect(raise_error).toRaise(KeyError, expectedMessageMatches = regexp)

    def test_expected_exception_with_message_not_matching_compiled_regexp_fails(self):
        message = ""
        regexp = re.compile("^not")
        try:
            expect(raise_error).toRaise(KeyError, expectedMessageMatches = regexp)
        except AssertionError as ex:
            message = ex.args[0]
            
        expect(message).toEqual("Expected <function raise_error>"
                                " to raise an instance of <class 'KeyError'>"
                                " with message matching regular expression '^not'"
                                ", but it raised an instance of <class 'KeyError'>"
                                " with message 'The wrong key was presented'")


class DefaultNotExpectationsTests(TestCase):
    def __init__(self, testFunctionName):
        TestCase.__init__(self, testFunctionName)

    def test_fail_doesnt_raise_anything(self):
        expect(True).Not.fail()
        # pass condition should be that we get to this point

    def test_success_raises_AssertionError(self):
        expect(lambda: expect(True).Not.success("Message")).toRaise(
                AssertionError,
                expectedMessage = "Message")

    def test_expect_truthy_values_not_to_be_true_fails(self):
        values = (True, 1, (1))
        expectedMessages = ("Expected True not to be True",
                          "Expected 1 not to be True", 
                          "Expected (1) not to be True")
        for i in range(0, len(expectedMessages) - 1):
            userMessage = "Index {}".format(i)
            expect(lambda: expect(values[i]).Not.toBeTrue()).toRaise(
                AssertionError,
                userMessage = userMessage,
                expectedMessage = expectedMessages[i])

    def test_expect_falsy_values_not_to_be_true_succeeds(self):
        values = (False, 0, ())
        for value in values:
            expect(value).Not.toBeTrue()

    def test_expect_truthy_values_not_to_be_false_succeeds(self):
        values = (True, 1, (1))
        for value in values:
            expect(value).Not.toBeFalse()

    def test_expect_falsy_values_not_to_be_false_fails(self):
        values = (False, 0, ())
        expectedMessages = ("Expected False not to be False",
                          "Expected 0 not to be False", 
                          "Expected () not to be False")
        for i in range(1, len(values) - 1):
            expect(lambda: expect(values[i]).Not.toBeFalse()).toRaise(
                AssertionError,
                userMessage = "Index {}".format(i),
                expectedMessage = expectedMessages[i])

    def test_expect_not_true_prepends_usermessage_to_assertion(self):
        expect(lambda: expect(True).withUserMessage("user message").Not.toBeTrue()).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expect_not_false_prepends_usermessage_to_assertion(self):
        expect(lambda: expect(False).withUserMessage("user message").Not.toBeFalse()).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expect_not_False_toBeNone_passes(self):
        expect(False).Not.toBeNone()

    def test_expect_not_None_toBeNone_fails_with_correct_message(self):
        expect(lambda: expect(None).Not.toBeNone()).toRaise(
            AssertionError,
            expectedMessage = "Expected None not to be None")

    def test_expect_not_toBeNone_prepends_userMessage(self):
        expect(lambda: expect(None).Not.toBeNone("user message")).toRaise(
            AssertionError,
            expectedMessageMatches = "^user message")

    def test_expect_not_1_instanceof_float_passes(self):
        # TODO: this should be expectNot
        expect(1).Not.toBeAnInstanceOf(float)

    def test_expect_not_1_instanceof_int_fails(self):
        expect(lambda: expect(1).Not.toBeAnInstanceOf(int)).toRaise(
            AssertionError,
            expectedMessage = "Expected 1 not to be an instance of <class 'int'>"
            " but was an instance of <class 'int'>")

    def test_expect_not_self_instanceof_TestResults_passes(self):
        expect(self).Not.toBeAnInstanceOf(TestResults)

    def test_expect_not_self_instanceof_ExpectNotTests_fails(self):
        expect(lambda: expect(self).Not.toBeAnInstanceOf(DefaultNotExpectationsTests)).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected <.*DefaultNotExpectationsTests object> "
            "not to be an instance of <class '.*DefaultNotExpectationsTests'> "
            "but was an instance of <class '.*DefaultNotExpectationsTests'>")

    def test_expect_not_self_instanceof_TestCase_fails(self):
        expect(lambda: expect(self).Not.toBeAnInstanceOf(TestCase)).toRaise(
            AssertionError,
            expectedMessageMatches = "Expected <.*DefaultNotExpectationsTests object>"
            " not to be an instance of <class '.*TestCase'>"
            " but was an instance of <class '.*DefaultNotExpectationsTests'>")        

    def test_instance_of_prepends_usermessage(self):
        expect(lambda: expect(1).Not.toBeAnInstanceOf(
                int, 
                "user message")).toRaise(
                AssertionError,
                expectedMessageMatches = "^user message")

    def test_expect_not_exception_raised_passes_if_exception_not_raised(self):
        expect(lambda: None).Not.toRaise(Exception)

    def test_expect_not_exception_fails_if_exact_exception_raised(self):
        message = ""
        try:
            expect(raise_error).Not.toRaise(KeyError)
        except AssertionError as ex:
            message = ex.args[0]
            
        expect(message).toEqual("Expected <function raise_error> "
            "not to raise an instance of <class 'KeyError'>"
            ", but it raised an instance of <class 'KeyError'>")

    def test_expect_not_exception_prepends_usermessage_when_exact_exception_raised(self):
        message = ""
        try:
            expect(raise_error).Not.toRaise(KeyError, "user message")
        except AssertionError as ex:
            message = ex.args[0]

        expect(message).toEqual("user message: "
                                "Expected <function raise_error>"
                                " not to raise an instance of <class 'KeyError'>"
                                ", but it raised an instance of <class 'KeyError'>")

    def test_expected_exception_with_unexpected_message_passes(self):
        expect(raise_error).Not.toRaise(KeyError, expectedMessage = "This is not the right message")

    def test_expected_exception_with_expected_message_fails(self):
        message = ""
        try:
            expect(raise_error).Not.toRaise(KeyError, expectedMessage = "The wrong key was presented")
        except AssertionError as ex:
            message = ex.args[0]

        expect(message).toEqual("Expected <function raise_error>"
                                " not to raise an instance of <class 'KeyError'>"
                                " with message 'The wrong key was presented'"
                                ", but it raised an instance of <class 'KeyError'>"
                                " with message 'The wrong key was presented'")

    def test_expect_not_exception_with_message_not_matching_regexp_passes(self):
        expect(raise_error).Not.toRaise(KeyError, expectedMessageMatches = "^not")

    def test_expect_not_raises_fails_if_error_matches_and_message_matches_regexp(self):
        message = ""
        try:
            expect(raise_error).Not.toRaise(KeyError, expectedMessageMatches = ".*")
        except AssertionError as ex:
            message = ex.args[0]

        expect(message).toEqual("Expected <function raise_error>"
                                " not to raise an instance of <class 'KeyError'>"
                                " with message matching regular expression '.*'"
                                ", but it raised an instance of <class 'KeyError'>"
                                " with message 'The wrong key was presented'")
