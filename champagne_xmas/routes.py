from flask import render_template, url_for, flash, redirect, session
from champagne_xmas.forms import RegistrationForm, LoginForm
from champagne_xmas.db import build_insert, load_user, get_users, all_users_here, get_pair, get_existing_pair
from champagne_xmas import app, bcrypt

@app.route("/")
def to_home():
    return redirect(url_for('home'))

@app.route("/home", defaults={'name' : None})
@app.route("/home/<name>")
def home(name):
    users = None
    user = None
    ready = None
    pair = None
    if 'user' in session:
        users = get_users()
        user = session['user']
        ready = all_users_here()
        pair = get_existing_pair(user)
        if name:
            pair = get_pair(user)
    return render_template('home.html', title='Home', user=user, users=users, ready=ready, pair=pair)


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