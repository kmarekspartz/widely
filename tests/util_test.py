from unittest import TestCase

from widely.util import NO_RESPONSES, YES_RESPONSES, get_y_or_n, sizeof_fmt
from util import StartsWithAssertion, IOStubs


class UtilTest(TestCase, StartsWithAssertion, IOStubs):
    def setUp(self):
        self.clear_log()
        self.clear_unknown_inputs_count()

    def test_yes_responses(self):
        for yes in ['y', 'Y', 'Yes', 'yes']:
            self.assertIn(yes, YES_RESPONSES)
            self.assertNotIn(yes, NO_RESPONSES)

    def test_no_responses(self):
        for no in ['n', 'N', 'No', 'no']:
            self.assertIn(no, NO_RESPONSES)
            self.assertNotIn(no, YES_RESPONSES)

    def test_message_defaults_to_continue(self):
        get_y_or_n(input=self.yes_input, output=self.log_output)
        self.assertStartsWith('Continue? (y/n)', self.full_log())

    def test_message_appends_a_space_when_passing_in_a_message(self):
        get_y_or_n(message='abc', input=self.yes_input, output=self.log_output)
        self.assertStartsWith('abc ', self.full_log())

    def test_returns_true_for_yes_input(self):
        self.assertTrue(
            get_y_or_n(
                input=self.yes_input,
                output=self.log_output
            )
        )

    def test_returns_false_for_no_input(self):
        self.assertFalse(
            get_y_or_n(
                input=self.no_input,
                output=self.log_output
            )
        )

    def test_looping_when_unknown_input(self):
        get_y_or_n(input=self.eventual_yes_input, output=self.log_output)
        self.assertEqual(
            'Continue? (y/n) ' +
            'Please enter y/n.' +
            'Continue? (y/n) ' +
            'Please enter y/n.' +
            'Continue? (y/n) ',
            self.full_log()
        )

    def test_sizeof_fmt(self):
        self.assertEqual('1000.0 bytes', sizeof_fmt(10 ** 3))
        self.assertEqual('976.6 KB', sizeof_fmt(10 ** 6))
        self.assertEqual('953.7 MB', sizeof_fmt(10 ** 9))
        self.assertEqual('931.3 GB', sizeof_fmt(10 ** 12))
        self.assertEqual('909.5 TB', sizeof_fmt(10 ** 15))
        self.assertEqual('909494.7 TB', sizeof_fmt(10 ** 18))
