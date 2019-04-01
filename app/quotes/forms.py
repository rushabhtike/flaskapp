from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, DateField, Label
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.models import User, UserProfile

class QuoteForm(FlaskForm):
    gallons_requested = IntegerField('Gallons Requested', validators=[DataRequired()])
    delivery_address = StringField('Delivery Address', render_kw={'readonly': True})
    date_requested = IntegerField('Date Requested', validators=[DataRequired()])
    suggested_price = IntegerField('Suggested Price', validators=[DataRequired()])
    total_amount_due = IntegerField('Total Amount Due', validators=[DataRequired()])
    submit = SubmitField('Get Quote')