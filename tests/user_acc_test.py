from app.db import db
from app.db.models import User
import os
import io
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user


def test_access_account_page_without_authenticated_user(client, application):
    response = client.get("/account", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/login'
    assert b'Please log in to access this page.' in response.data
    assert b'<h2>Login</h2>' in response.data


def test_access_accout_page_after_authenticated(client, application):
    user_setup_and_login(client)
    response = client.get("/account", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/account'
    assert b'Manage Account' in response.data
    assert b'You can change your email address' in response.data
    assert b'Create a password' in response.data
    assert b'Please retype your password to confirm it is correct' in response.data
    assert b'Submit' in response.data


def test_update_account(client, application):
    user_setup_and_login(client)
    assert db.session.query(User).count() == 1
    user = User.query.filter_by(email='test@mail.com').first()
    assert user.email == 'test@mail.com'

    response = client.post('/account', data={
        'email': 'mytest@mail.com',
        'password': 'abc1234',
        'confirm': 'abc1234'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/dashboard'
    assert b'You Successfully Updated your Password or Email' in response.data

    assert db.session.query(User).count() == 1
    user = User.query.filter_by(email='test@mail.com').first()
    assert user is None

    user = User.query.filter_by(email='mytest@mail.com').first()
    assert user is not None


def user_setup_and_login(client):
    assert db.session.query(User).count() == 0
    user = User('test@mail.com', generate_password_hash('123456'))
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
