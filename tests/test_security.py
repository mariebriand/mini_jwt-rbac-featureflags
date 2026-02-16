import pytest

from app.core.security import hash_password, verify_password


def test_hash_and_verify_success():
    password = "Secret123!"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword", hashed)


def test_empty_password_raises():
    with pytest.raises(ValueError):
        hash_password("")

    with pytest.raises(ValueError):
        hash_password("   ")


def test_long_password_hash_and_verify_success():
    # bcrypt has a 72-byte limit; we pre-hash, so long passwords must still work
    long_pw = "a" * 200 + "A1!"
    hashed = hash_password(long_pw)
    assert hashed != long_pw
    assert verify_password(long_pw, hashed)
    assert not verify_password("a" * 200 + "Wrong", hashed)


def test_unicode_normalization_equivalence_success():
    # 'é' as single codepoint vs 'e' + combining acute accent should be treated the same
    pw1 = "Café123!"
    pw2 = "Cafe\u0301123!"  # e + combining acute
    hashed = hash_password(pw1)
    assert verify_password(pw2, hashed)


def test_malformed_hash_returns_false():
    # verify_password should be defensive and return False for malformed/stub hashes
    assert verify_password("Secret123!", "not_a_valid_hash") is False
