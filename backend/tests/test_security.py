from app.security import hash_password, verify_password


def test_password_is_hashed_and_can_be_verified():
    password = "CampusNest-example-password"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password) is True


def test_wrong_password_is_rejected():
    hashed_password = hash_password("correct-password")

    assert verify_password("wrong-password", hashed_password) is False


def test_same_password_gets_different_salted_hashes():
    first_hash = hash_password("same-password")
    second_hash = hash_password("same-password")

    assert first_hash != second_hash
    assert verify_password("same-password", first_hash) is True
    assert verify_password("same-password", second_hash) is True
