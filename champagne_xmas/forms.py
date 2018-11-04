from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):           
    username = StringField('Felhasználónév', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Jelszó', validators=[DataRequired()])
    confirm_password = PasswordField('Jelszó megerősítés', validators=[DataRequired(), EqualTo('password')])   
    vipcode = PasswordField('VIP kód', validators=[DataRequired()])
    submit = SubmitField('Regisztráció')

class LoginForm(FlaskForm):
    username = StringField('Felhasználónév', validators=[DataRequired()])
    password = PasswordField('Jelszó', validators=[DataRequired()])
    submit = SubmitField('Belépés')

class RoomForm(FlaskForm):
    roomname = StringField('Szoba neve', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email cím', validators=[DataRequired(), Email()])
    letszam = IntegerField('Résztvevők száma (fontos)', validators=[DataRequired()])
    vipcode = PasswordField('VIP kód', validators=[DataRequired()])
    submit = SubmitField('Szoba létrehozás')