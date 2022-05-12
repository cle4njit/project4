from app.db import db
from app.db.models import User, AccountTransaction
import os
import io
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user


def test_access_upload_transaction_without_authenticated_user(client, application):
    response = client.get("/account/transaction/upload", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/login'
    assert b'Please log in to access this page.' in response.data
    assert b'<h2>Login</h2>' in response.data


def test_access_upload_transaction_after_authenticated(client, application):
    user_setup_and_login(client)
    response = client.get("/account/transaction/upload", follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/account/transaction/upload'
    assert b'File' in response.data
    assert b'Upload Transactions' in response.data


def test_upload_transaction_csv(client, application):
    user_setup_and_login(client)
    assert db.session.query(AccountTransaction).count() == 0
    user = User.query.filter_by(email='test@mail.com').first()
    assert user.account_balance == 0

    # Read CSV file from system
    test_dir = os.path.join(os.getcwd(), 'tests')
    with open(test_dir + "/transactions-test.csv", encoding='utf-8-sig') as f:
        file_content = f.read()

    # Submit CSV file POST call
    file_name = "transactions.csv"
    data = {
        'file': (io.BytesIO(file_content.encode()), file_name)
    }
    response = client.post('/account/transaction/upload', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/dashboard'

    # transactions saved in db, 5 transaction were present in csv
    transactions = AccountTransaction.query.all()
    assert len(transactions) == 5

    # 5 transaction for current user & updated account balance.
    assert db.session.query(AccountTransaction).count() == 5
    user = User.query.filter_by(email='test@mail.com').first()
    assert user.account_balance == 2500

    # file uploaded to uploads directory
    root = os.getcwd()
    upload_dir = os.path.join(os.getcwd(), 'uploads')
    assert os.path.exists(upload_dir) == True
    assert os.path.exists(os.path.join(upload_dir, file_name)) == True


def user_setup_and_login(client):
    assert db.session.query(User).count() == 0
    user = User('test@mail.com', generate_password_hash('123456'))
    db.session.add(user)
    db.session.commit()
    assert db.session.query(User).count() == 1
    # finding one user record by email
    user = User.query.filter_by(email='test@mail.com').first()
    # asserting that the user retrieved is correct
    assert user.email == 'test@mail.com'

    # login with newly registered user
    response = client.post('/login', data={
        'email': 'test@mail.com',
        'password': '123456',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/dashboard'
    html = response.get_data(as_text=True)
    assert '<p>Welcome: test@mail.com</p>' in html
