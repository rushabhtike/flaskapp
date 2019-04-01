from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.models import User, UserProfile


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UpdateAccountForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # email = StringField('Email', validators=[DataRequired(), Email()])

    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=50)])
    address_one = StringField('Address 1', validators=[DataRequired(), Length(max=100)])
    address_two = StringField('Address 2', validators=[Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State', validators=[DataRequired(), Length(max=2)])
    zipcode = IntegerField('Zipcode', validators=[DataRequired()])

    submit = SubmitField('Update')

    # def validate_username(self, username):
    #     if username.data != current_user.username:
    #         user = User.query.filter_by(username=username.data).first()
    #         if user:
    #             raise ValidationError('Username already exists')
    #
    # def validate_email(self, email):
    #     if email.data != current_user.email:
    #         user = User.query.filter_by(email=email.data).first()
    #         if user:
    #             raise ValidationError('Email already exists')
