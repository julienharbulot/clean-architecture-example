from datetime import datetime, timedelta
from unittest import TestCase

from src.business_layer.errors import ErrorCode
from src.business_layer.policies import (
    birthdate_validation_policy,
    email_validation_policy,
    password_validation_policy,
    user_activation_timeout_policy,
)


class TestPasswordValidationPolicy(TestCase):
    def test_password_valid(self):
        password = "12345678aA+"
        e = password_validation_policy(password)
        self.assertFalse(e)

    def test_missing_char(self):
        password = "12345678"
        e = password_validation_policy(password)
        self.assertEqual(e, [ErrorCode.password_does_not_contain_char])

    def test_missing_number(self):
        password = "abcd efgh"
        e = password_validation_policy(password)
        self.assertEqual(e, [ErrorCode.password_does_not_contain_number])

    def test_too_small_and_missing_number(self):
        password = "a"
        e = password_validation_policy(password)
        self.assertEqual(
            set(e),
            {
                ErrorCode.password_does_not_contain_number,
                ErrorCode.password_is_less_than_8_chars,
            },
        )


class TestEmailValidationPolicy(TestCase):
    def test_valid_email(self):
        email = "julien.harbulot@mygmail.com"
        e = email_validation_policy(email)
        self.assertFalse(e)

    def test_missing_at(self):
        email = "julien.harbulotmygmail.com"
        e = email_validation_policy(email)
        self.assertEqual(e, [ErrorCode.email_invalid])

    def test_missing_extension(self):
        email = "julien.harbulot@mygmailcom"
        e = email_validation_policy(email)
        self.assertEqual(e, [ErrorCode.email_invalid])


class TestBirthdateValidationPolicy(TestCase):
    def test_too_young(self):
        for age in range(-5, 18):
            birthdate = datetime.now() - timedelta(age * 365)
            e = birthdate_validation_policy(birthdate)
            self.assertEqual(e, [ErrorCode.less_than_18_years_old])

    def test_ok(self):
        for age in range(18, 100):
            birthdate = datetime.now() - timedelta(age * 365)
            e = birthdate_validation_policy(birthdate)
            self.assertFalse(e)

    def test_too_old(self):
        for age in range(100, 120):
            birthdate = datetime.now() - timedelta(age * 365)
            e = birthdate_validation_policy(birthdate)
            self.assertEqual(e, [ErrorCode.more_than_100_years_old])


class TestUserActivationTimeoutPolicy(TestCase):
    def test_no_timeout(self):
        created = datetime.now() - timedelta(hours=12)
        activated = datetime.now()
        timeout = user_activation_timeout_policy(created, activated)
        self.assertFalse(timeout)

    def test_timeout(self):
        created = datetime.now() - timedelta(hours=73)
        activated = datetime.now()
        timeout = user_activation_timeout_policy(created, activated)
        self.assertTrue(timeout)

    def test_created_after_activated_no_timeout(self):
        created = datetime.now()
        activated = datetime.now() - timedelta(hours=80)
        timeout = user_activation_timeout_policy(created, activated)
        self.assertFalse(timeout)
