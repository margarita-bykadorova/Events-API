from models import User


def test_user_password_hashing_and_verification():
    user = User(username="test")

    user.set_password("pass")

    assert user.password_hash != "pass"
    assert user.check_password("pass") is True
    assert user.check_password("wrong") is False
