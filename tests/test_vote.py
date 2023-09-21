import pytest

from app import models


@pytest.fixture()
def test_vote(created_posts, session, test_user):
    new_vote = models.Votes(post_id=created_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, created_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": created_posts[3].id, "vote_dir": 1})
    assert res.status_code == 200


def test_vote_twice_post(authorized_client, created_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": created_posts[3].id, "vote_dir": 1})
    assert res.status_code == 409


def test_delete_vote(authorized_client, created_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": created_posts[3].id, "vote_dir": 0})
    assert res.status_code == 200


def test_vote_non_exist_post(authorized_client, created_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": 99999, "vote_dir": 0})
    assert res.status_code == 404


def test_delete_vote_non_exist(authorized_client, created_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": 99999, "vote_dir": 0})
    assert res.status_code == 404


def test_vote_unauthorized_user(client, created_posts):
    res = client.post(
        "/vote/", json={"post_id": created_posts[3].id, "vote_dir": 1})
    assert res.status_code == 401
