from app.db import db
from app.db.models import User
import os
import io
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user


def test_access_users_page_without_authenticated_user(client):
    response = client.get("/users", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/login'
    assert b'Please log in to access this page.' in response.data
    assert b'<h2>Login</h2>' in response.data


def test_access_users_page_after_authenticated(client):
    user_setup_and_login(client)
    response = client.get("/users", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/users'
    assert b'<h2>Browse: Users</h2>' in response.data
    assert b'Email' in response.data
    assert b'Registered On' in response.data
    assert b'Actions' in response.data
    assert b'test@mail.com' in response.data


def test_view_user(client):
    user_setup_and_login(client)
    response = client.get("/users/1", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/users/1'
    assert b'<h2>User profile</h2>' in response.data
    assert b'User Email: test@mail.com' in response.data


def test_edit_user(client):
    user_setup_and_login(client)
    user = User.query.filter_by(email='test@mail.com').first()
    assert user.about is None
    response = client.post('/users/1/edit', data={
        'about': 'This my profile to test',
        'is_admin': 1
    }, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/users'
    assert b'User Edited Successfully' in response.data
    user = User.query.filter_by(email='test@mail.com').first()
    assert user.about == 'This my profile to test'


def test_add_user(client):
    user_setup_and_login(client)
    user = User.query.filter_by(email='mytestadd@mail.com').first()
    assert db.session.query(User).count() == 1
    assert user is None
    response = client.post('/users/new', data={
        'email': 'mytestadd@mail.com',
        'password': '123456',
        'confirm': '123456'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/users'
    assert b'Congratulations, you just created a user' in response.data
    user = User.query.filter_by(email='mytestadd@mail.com').first()
    assert db.session.query(User).count() == 2
    assert user is not None
    assert user.email == 'mytestadd@mail.com'


def test_add_user_already_exist(client):
    user_setup_and_login(client)
    user = User.query.filter_by(email='test@mail.com').first()
    assert db.session.query(User).count() == 1
    assert user is not None
    assert user.email == 'test@mail.com'

    response = client.post('/users/new', data={
        'email': 'test@mail.com',
        'password': '123456',
        'confirm': '123456'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/users'
    assert b'Already Registered' in response.data
    assert db.session.query(User).count() == 1


def test_delete_user_self(client):
    user_setup_and_login(client)
    user = User.query.filter_by(email='test@mail.com').first()
    assert db.session.query(User).count() == 1
    assert user is not None
    assert user.email == 'test@mail.com'

    response = client.post("/users/1/delete", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/users'
    html = response.get_data(as_text=True)
    assert 'You can&#39;t delete yourself!' in html
    assert db.session.query(User).count() == 1


def test_delete_user(client):
    test_add_user(client)
    user = User.query.filter_by(email='mytestadd@mail.com').first()
    assert db.session.query(User).count() == 2
    assert user is not None
    assert user.id == 2

    response = client.post("/users/2/delete", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/users'
    assert b"User Deleted" in response.data
    user = User.query.filter_by(email='mytestadd@mail.com').first()
    assert db.session.query(User).count() == 1
    assert user is None


def user_setup_and_login(client):
    assert db.session.query(User).count() == 0
    user = User('test@mail.com', generate_password_hash('123456'))
    user.is_admin = 1
    db.session.add(user)
    db.session.commit()
    assert db.session.query(User).count() == 1
    user = User.query.filter_by(email='test@mail.com').first()
    assert user.email == 'test@mail.com'

    response = client.post('/login', data={
        'email': 'test@mail.com',
        'password': '123456',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/dashboard'
    html = response.get_data(as_text=True)
    assert '<p>Welcome: test@mail.com</p>' in html
