from flask import render_template, url_for, flash, redirect, session
from champagne_xmas.forms import RegistrationForm, LoginForm, RoomForm
from champagne_xmas.db import build_insert, load_user, get_users, all_users_here, get_pair, get_existing_pair, save_room, get_roomname
from champagne_xmas import app, bcrypt
from champagne_xmas.logic import send_email

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
    roomname = "Minden ami zokni"
    if 'user' in session:
        users = get_users(session['room'])
        user = session['user']
        ready = all_users_here(session['room'])
        pair = get_existing_pair(user, session['room'])
        roomname = get_roomname(session['room'])
        if name and ready and not pair:
            pair = get_pair(user, session['room'])
    return render_template('home.html', title='Home', user=user, users=users, ready=ready, pair=pair, roomname = roomname)


@app.route("/regisztracio", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        result = build_insert(form.username.data, hashed_password, form.vipcode.data)
        if result == "nev":
            flash('Valaki ezzel a névvel már regisztrált bocsi!', 'danger')
            return redirect(url_for('register')) 
        if result == "room":
            flash('Vip kód nem megfelelő!', 'danger')
            return redirect(url_for('register'))
        flash(f'Üdv a csapatban {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Regisztráció')


@app.route("/beljelentkezes", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = load_user( form.username.data, form.password.data)
        if result:
            session['user'] = form.username.data
            session['room'] = result
            return redirect(url_for('home'))
        else:
            flash('Sikerltelen bejelentkezés', 'danger')
    return render_template('login.html', form=form, title='Belépés')

@app.route("/kijelentkezes")
def logout():
    del session['user']
    del session['room']
    return redirect(url_for('home'))

@app.route("/szoba", methods=['GET', 'POST'])
def create_room():
    form = RoomForm()
    if form.validate_on_submit():
        if save_room(form.roomname.data, form.vipcode.data, form.letszam.data):
            flash("Szoba sikeresen létrehozva. Hamarosan kapni fogsz emailt a részletekkel!", "success")
            send_email(form.email.data, form.roomname.data, form.vipcode.data)
            return redirect(url_for('home'))
        flash("Ilyen nevű szoba sajna már létezik, válassz mást!", "danger")
        return redirect(url_for('create_room'))
    return render_template("room.html", form=form)