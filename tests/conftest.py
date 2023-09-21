import pytest
from fastapi.testclient import TestClient
from app import models
from app.database import get_db
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Settings as St
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{St.db_username}:{St.db_password}@{St.db_hostname}:{St.db_port}/{St.db_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client) -> dict:
    user_data = {"email": "daniel@cuyama.com", "password": "12345"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user_2(client):
    user_data = {"email": "daniel1@cuyama.com", "password": "12345"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def created_posts(test_user, test_user_2, session):
    posts_data = [
        {"title": "first title",
         "content": "first content",
         "user_id": test_user['id']},
        {"title": "2nd title",
         "content": "2nd content",
         "user_id": test_user['id']},
        {"title": "3rd title",
         "content": "3rd content",
         "user_id": test_user['id']},
        {"title": "4rd title",
         "content": "4rd content",
         "user_id": test_user_2['id']}
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
