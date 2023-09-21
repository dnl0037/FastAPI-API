from jose import jwt
from app.config import Settings as St
from app import schemas
import pytest


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "daniel123@cuyama.com", "password": "12345"})
    new_user = schemas.CreatedUser(**res.json())
    assert new_user.email == "daniel123@cuyama.com"
    assert res.status_code == 201


def test_login(client, test_user):
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    token = schemas.Token(**response.json())
    decoded_payload = jwt.decode(token.access_token, St.secret_key, [St.algorithm])
    decoded_payload_id = decoded_payload.get("user_id", None)
    assert response.status_code == 200
    assert decoded_payload_id == test_user["id"]
    assert token.token_type == "bearer"


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', '12345', 403),
    ('daniel@cuyama.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, '12345', 422),
    ('daniel@cuyama.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code
