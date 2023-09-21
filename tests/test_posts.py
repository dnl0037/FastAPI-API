from app import schemas
import pytest


def test_get_all_posts_empty(authorized_client):
    response = authorized_client.get("/posts/")
    assert response.json()["detail"] == "No posts found"
    assert response.status_code == 404


def test_get_all_posts(authorized_client, created_posts):
    response = authorized_client.get("/posts/")
    # posts = [schemas.PostComplete(**post) for post in response.json()]
    assert response.status_code == 202
    assert len(response.json()) == len(created_posts)


def test_unathorized_user_get_all_posts(client, created_posts):
    response = client.get("/posts/")
    assert response.status_code == 401


def test_unathorized_user_get_one_post(client, created_posts):
    response = client.get(f"/posts/{created_posts[0].id}")
    assert response.status_code == 401


def test__user_get_non_existent_post(authorized_client, created_posts):
    response = authorized_client.get("/posts/2323212")
    assert response.status_code == 404


def test_user_get_one_post(authorized_client, created_posts):
    response = authorized_client.get(f"/posts/{created_posts[0].id}")
    post = schemas.PostComplete(**response.json())
    assert response.status_code == 202
    assert post.Post.id == created_posts[0].id
    assert post.Post.content == created_posts[0].content
    assert post.Post.title == created_posts[0].title


@pytest.mark.parametrize(
    "title, content, published",
    [("Primer titulo", "Primer contenido", True),
     ("Segundo titulo", "Segundo Contenido", False),
     ("Tecer titulo", "Tercer contenido", True)])
def test_create_post(authorized_client, test_user, created_posts, title, content, published):
    response = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    post = schemas.CreatedPost(**response.json())
    assert response.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.user_id == test_user["id"]


@pytest.mark.parametrize(
    "title, content",
    [("Primer titulo", "Primer contenido"),
     ("Segundo titulo", "Segundo Contenido"),
     ("Tecer titulo", "Tercer contenido")])
def test_create_post_default_published(authorized_client, test_user, created_posts, title, content):
    response = authorized_client.post("/posts/", json={"title": title, "content": content})
    post = schemas.CreatedPost(**response.json())
    assert response.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.published is True
    assert post.user_id == test_user["id"]


def test_unauthorized_user_create_post(client):
    response = client.post("/posts/", json={"title": "Hola", "content": "Como estas"})
    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, created_posts):
    response = client.delete(f"/posts/{created_posts[0].id}")
    assert response.status_code == 401


def test_authorized_user_delete_post(authorized_client, created_posts):
    response = authorized_client.delete(f"/posts/{created_posts[0].id}")
    assert response.status_code == 204


def test_authorized_user_delete_non_existent_post(authorized_client):
    response = authorized_client.delete(f"/posts/55555")
    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, created_posts):
    response = authorized_client.delete(f"/posts/{created_posts[3].id}")
    assert response.status_code == 403


def test_unauthorized_user_update_post(client, created_posts):
    response = client.put(f"/posts/{created_posts[0].id}",
                          json={"title": "Nuevo titulo", "content": "Nuevo contenido", "published": True})
    assert response.status_code == 401


def test_authorized_user_update_post(authorized_client, created_posts, test_user):
    response = authorized_client.put(f"/posts/{created_posts[0].id}",
                                     json={"title": "Nuevo titulo", "content": "Nuevo contenido",
                                           "published": True})
    new_post = schemas.CreatedPost(**response.json())
    assert new_post.user_id == test_user["id"]
    assert new_post.title == "Nuevo titulo"
    assert new_post.content == "Nuevo contenido"
    assert new_post.published is True


def test_authorized_user_update_non_existent_post(authorized_client, created_posts, test_user):
    response = authorized_client.put(f"/posts/5555555555555",
                                     json={"title": "Nuevo titulo", "content": "Nuevo contenido",
                                           "published": True})
    assert response.status_code == 404


def test_authorized_user_update_other_user_post(authorized_client, created_posts, test_user):
    response = authorized_client.put(f"/posts/{created_posts[3].id}",
                                     json={"title": "Nuevo titulo", "content": "Nuevo contenido",
                                           "published": True})
    assert response.status_code == 403
