from app.db import db
from app.db.models import User
import os
import io


def test_access_login_page(client):
    """This makes the login page"""
    response = client.get("/login")
    assert response.status_code == 200
    assert b'<h2>Login</h2>' in response.data


def test_login_and_redirect_to_dashboard(client, application):
    # first register user before login
    response = client.post('/register', data={
        'email': 'test@mail.com',
        'password': '123456',
        'confirm': '123456'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/login'

    # login
    # login with newly regitered user
    response = client.post('/login', data={
        'email': 'test@mail.com',
        'password': '123456',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/dashboard'
    html = response.get_data(as_text=True)
    assert '<p>Welcome: test@mail.com</p>' in html

    # after login access dashboard page
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/dashboard'
    html = response.get_data(as_text=True)
    assert '<p>Welcome: test@mail.com</p>' in html


def test_user_logout_without_authenticated_user(client, application):
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/login'
    assert b'Please log in to access this page.' in response.data
    assert b'<h2>Login</h2>' in response.data


def test_user_logout(client, application):
    # first login before to logout
    test_login_and_redirect_to_dashboard(client, application)

    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/login'
    assert b'<h2>Login</h2>' in response.data
