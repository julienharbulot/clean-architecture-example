from typing import Callable

from src.business_layer.models import User, UserRequiredInfo


def assert_matching(user: User, create_data: UserRequiredInfo, assert_equal: Callable):
    assert_equal(user.info.email, create_data.email)
    assert_equal(user.info.name, create_data.name)
    assert_equal(user.info.birthdate, create_data.birthdate)
