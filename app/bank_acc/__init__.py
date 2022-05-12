import csv
import logging
import os

from flask import Blueprint, render_template, abort, url_for, current_app
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.db import db
from app.db.models import AccountTransaction
from app.bank_acc.forms import csv_upload
from werkzeug.utils import secure_filename, redirect

bank_account = Blueprint('bank_acc', __name__,
                         template_folder='templates')


@bank_account.route('/accounts/all', methods=['GET'], defaults={"page": 1})
@bank_account.route('/accounts/all/<int:page>', methods=['GET'])
@login_required
def browse_account_transactions(page):
    page = page
    per_page = 1000
    pagination = AccountTransaction.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        return render_template('browse_accounts.html', data=data, pagination=pagination)
    except TemplateNotFound:
        abort(404)


@bank_account.route('/account/transaction/upload', methods=['POST', 'GET'])
@login_required
def transaction_upload():
    form = csv_upload()
    if form.validate_on_submit():
        log = logging.getLogger("myApp")

        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        log.info('Bank acc transaction file uploaded filepath: ' + filepath)

        with open(filepath, encoding='utf-8-sig') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                amount = int(row['AMOUNT'])
                transaction_type = row['TYPE']
                current_user.account_balance += amount
                current_user.account_transaction.append(AccountTransaction(amount, transaction_type, current_user.id))
                db.session.commit()

        return redirect(url_for('auth.dashboard'))

    try:
        return render_template('upload.html', form=form)
    except TemplateNotFound:
        abort(404)


@bank_account.route('/account/transaction/delete', methods=['POST', 'GET'])
@login_required
def transaction_delete():
    AccountTransaction.query.filter_by(user_id=current_user.id).delete()
    current_user.account_balance = 0
    db.session.commit()
    log = logging.getLogger("myApp")
    log.info('My all transactions has been deleted - Account reset')

    return redirect(url_for('auth.dashboard'))
