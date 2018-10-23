from flask import render_template, url_for, flash, redirect, session
from champagne_xmas.forms import RegistrationForm, LoginForm
from champagne_xmas.db import build_insert, load_user
from champagne_xmas import app

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home', user=session['user'] if 'user' in session else None)


@app.route("/regisztracio", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if not build_insert(form.username.data, hashed_password):
            flash('Valaki ezzel a névvel már regisztrált bocsi!', 'danger')
            return redirect(url_for('register'))   
        flash(f'Üdv a csapatban {form.username.data}!', 'success')
        session['user'] = form.username.data
        return redirect(url_for('home'))
    return render_template('register.html', form=form, title='Regisztráció')


@app.route("/beljelentkezes", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if load_user( form.username.data, form.password.data):
            session['user'] = form.username.data
            return redirect(url_for('home'))
        else:
            flash('Sikerltelen bejelentkezés', 'danger')
    return render_template('login.html', form=form, title='Belépés')

@app.route("/kijelentkezes")
def logout():
    del session['user']
    return redirect(url_for('home'))