from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class register_form(FlaskForm):
    email = EmailField('Email Address', [
        validators.DataRequired(),
    ], description="Please sign up with your email")

    password = PasswordField('Create Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
    ], description="Create a password ")
    confirm = PasswordField('Repeat Password', description="Please retype your password to ensure it is correct")
    submit = SubmitField()

class login_form(FlaskForm):
    email = EmailField('Email Address', [
        validators.DataRequired(),
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.length(min=6, max=35)
    ])
    submit = SubmitField()

class create_user_form(FlaskForm):
    email = EmailField('Email Address', [
        validators.DataRequired(),
    ], description="Please sign up with your email")

    password = PasswordField('Create Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
    ], description="Create a password ")
    confirm = PasswordField('Repeat Password', description="Please retype your password to ensure it is correct")
    is_admin = BooleanField('Admin', render_kw={'value':'1'})
    submit = SubmitField()

class profile_form(FlaskForm):
    about = TextAreaField('About', [validators.length(min=6, max=300)],
                          description="Add information about yourself")
    submit = SubmitField()

class user_edit_form(FlaskForm):
    about = TextAreaField('About', [validators.length(min=6, max=300)],
                          description="Add information about yourself")
    is_admin = BooleanField('Admin', render_kw={'value':'1'})
    submit = SubmitField()

class security_form(FlaskForm):
    email = EmailField('Email Address', [
        validators.DataRequired(),
    ], description="Feel free to change your email address")
    password = PasswordField('Create Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
    ], description="Create a password ")
    confirm = PasswordField('Repeat Password', description="Please retype your password to ensure it is correct")
    submit = SubmitField()

class csv_upload(FlaskForm):
    file = FileField()
    submit = SubmitField()