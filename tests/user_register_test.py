from app.db import db
from app.db.models import User
import os
import io


def test_access_register_page(client):
    """This makes the register page"""
    response = client.get("/register")
    assert response.status_code == 200
    assert b'<h2>Register</h2>' in response.data


def test_register_user(client, application):
    """Post user details to register"""
    response = client.post('/register', data={
        'email': 'test@mail.com',
        'password': '123456',
        'confirm': '123456'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/login'
    user = User.query.filter_by(email='test@mail.com').first()
    assert user is not None
    assert user.email == 'test@mail.com'
