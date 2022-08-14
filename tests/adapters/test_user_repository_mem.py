from datetime import datetime
from unittest import TestCase

from src.adapters.user_repository_mem import UserRepositoryMem
from src.business_layer.errors import Error, ErrorCode
from src.business_layer.models import UserRequiredInfo
from tests.utils import assert_matching

data1 = UserRequiredInfo("email", "name", datetime.now())
data2 = UserRequiredInfo("email2", "name2", datetime.now())


class TestUserRepositoryMem(TestCase):
    def test_when_ok(self):
        repo = UserRepositoryMem()
        uid = repo.create_user(data1, "security_id")

        user_by_email = repo.get_by_email(data1.email)
        user_by_id = repo.get_by_id(uid)

        assert_matching(user_by_email, data1, self.assertEqual)
        self.assertEqual(user_by_email, user_by_id)

    def test_when_two_users_ok(self):
        repo = UserRepositoryMem()
        uid1 = repo.create_user(data1, "security_id")
        uid2 = repo.create_user(data2, "security_id")

        self.assertNotEqual(uid1, uid2)
        assert_matching(repo.get_by_email(data1.email), data1, self.assertEqual)
        assert_matching(repo.get_by_email(data2.email), data2, self.assertEqual)

    def test_when_already_exists(self):
        repo = UserRepositoryMem()
        repo.create_user(data1, "security_id")

        with self.assertRaises(Error) as context:
            repo.create_user(data1, "security_id")

        self.assertEqual(context.exception.error_codes, [ErrorCode.user_exists])
