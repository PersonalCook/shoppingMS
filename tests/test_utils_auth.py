import os

import jwt
import pytest
from jwt import InvalidTokenError

from app.utils.auth import decode_jwt


def test_decode_jwt_valid():
    token = jwt.encode(
        {"user_id": 123},
        os.environ["JWT_SECRET"],
        algorithm=os.environ["JWT_ALGORITHM"],
    )

    payload = decode_jwt(token)
    assert payload["user_id"] == 123


def test_decode_jwt_invalid_signature():
    token = jwt.encode(
        {"user_id": 123},
        "wrong-secret",
        algorithm=os.environ["JWT_ALGORITHM"],
    )

    with pytest.raises(InvalidTokenError):
        decode_jwt(token)
