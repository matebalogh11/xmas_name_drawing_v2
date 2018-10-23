from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from db import build_insert

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ce2878bbd3b851fccf0a22304cc1f46c'
bcrypt = Bcrypt(app)

@app.route("/")
@app.route("/home")
def home():
    print("Going to home page")
    return render_template('home.html', title='Home')


@app.route("/regisztracio", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if not build_insert(form.username.data, hashed_password):
            flash('Valaki ezzel a névvel már regisztrált bocsi!', 'danger')
            return redirect(url_for('register'))   
        flash(f'Üdv a csapatban {form.username.data}!', 'success')
        return redirect(url_for('home'))
    else:
        print("Szar van a levesben")
    return render_template('register.html', form=form, title='Regisztráció')


@app.route("/beljelentkezes")
def login():
    form = LoginForm()
    return render_template('login.html', form=form, title='Belépés')


if __name__ == "__main__":
    app.run(debug=True)