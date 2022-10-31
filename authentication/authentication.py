from flask import render_template, redirect, session, url_for, request, session
from passlib.hash import sha256_crypt
import database.database as db
import random
import string


def authenticate_dashboard():
    return render_template('dashboard.html') if session.get('loggedin') else redirect('/login')


def handle_request():
    errorMessage = ''
    if request.method == 'POST' and 'username' in request.form and\
            'password' in request.form and\
            'email' in request.form and\
            'club' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        club = request.form['club']
        letters = string.ascii_lowercase
        db.store_account(''.join(random.choice(letters) for i in range(5)),
                         username, sha256_crypt.encrypt(password),
                         email, club)
        return redirect("/")
    else:
        return render_template('request.html')


def handle_login():
    loggedin = session.get('loggedin')
    if (loggedin):
        return redirect('/dashboard')

    errorMessage = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        account = db.request_account(username, password)

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['displayname'] = account['display_name']
            return render_template('dashboard.html')

        else:
            errorMessage = 'Uw gebruikersnaam of wachtwoord is fout.'
    return render_template('login.html', errorMessage=errorMessage)


def handle_logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('displayname', None)
    return redirect(url_for('login'))
