from dataclasses import replace

import pytest

from cryptosec_lab.passwords import (
    ALGORITHMS,
    hash_password,
    synthetic_password,
    verify_password,
)


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_salt_wrong_password_and_unicode(algorithm):
    password = synthetic_password() + "中文"
    first = hash_password(password, algorithm)
    second = hash_password(password, algorithm)
    assert first != second
    assert password not in first.digest
    assert verify_password(password, first)
    assert not verify_password(password + "!", first)
    with pytest.raises(ValueError):
        verify_password(password, replace(first, version=99))


def test_parameter_bomb_rejected_before_hashing():
    record = hash_password(synthetic_password())
    with pytest.raises(ValueError, match="profile"):
        verify_password(
            synthetic_password(),
            replace(record, digest=record.digest.replace("m=65536", "m=999999999")),
        )


def test_malformed_record():
    password = synthetic_password()
    record = hash_password(password, "pbkdf2")
    with pytest.raises(ValueError):
        verify_password(password, replace(record, salt=b"short"))
    with pytest.raises(ValueError):
        verify_password(password, replace(record, digest="not hex"))
    with pytest.raises(ValueError):
        verify_password(password, replace(record, digest="aa"))


@pytest.mark.parametrize("password", ["", "x" * 1025, "中" * 400])
def test_password_bound(password):
    with pytest.raises(ValueError):
        hash_password(password)


def test_unknown_algorithm():
    with pytest.raises(ValueError):
        hash_password(synthetic_password(), "md5")
