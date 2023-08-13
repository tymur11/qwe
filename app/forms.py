from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class Register(FlaskForm):
    user = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    button = SubmitField('Enter')


class Signin(FlaskForm):
    user = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    button = SubmitField('Enter')
    galochka = BooleanField('remember me')


class Game(FlaskForm):
    price = StringField('price', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    button = SubmitField('Enter')

