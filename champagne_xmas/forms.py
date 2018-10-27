from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):

    def validate_proof(form, field):
        if field.data != "alma":
            raise ValidationError('Nem tagoknak nem jár zokni!')
            
    username = StringField('Felhasználónév', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Jelszó', validators=[DataRequired()])
    confirm_password = PasswordField('Jelszó megerősítés', validators=[DataRequired(), EqualTo('password')])   
    submit = SubmitField('Regisztráció')
    proof = PasswordField('VIP kód', validators=[DataRequired(), validate_proof])

class LoginForm(FlaskForm):
    username = StringField('Felhasználónév', validators=[DataRequired()])
    password = PasswordField('Jelszó', validators=[DataRequired()])
    remember = BooleanField('Emlékezz rám')
    submit = SubmitField('Belépés')