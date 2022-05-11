from unittest import TestCase

from src.utils import PasswordUtils


class TestPasswordUtils(TestCase):
    def test_when_match(self):
        password = "12345arstdb./?= !!x"
        pw_hash = PasswordUtils.hash_password(password)
        self.assertTrue(PasswordUtils.is_correct_password(pw_hash, password))

    def test_when_no_match(self):
        password = "2345arstdb./?= !!x"
        pw_hash = PasswordUtils.hash_password(password)
        self.assertTrue(PasswordUtils.is_correct_password(pw_hash, password))
