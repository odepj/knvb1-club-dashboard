from flask import Flask, render_template
from authentication.authentication import authenticate_dashboard, handle_logout, handle_login
import render_templates


app = Flask(__name__)
app.secret_key = 'databaseproject'


@app.route('/')
def intro():
    return render_template('intro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return handle_login()


@app.route('/logout')
def logout():
    return handle_logout()


@app.route('/dashboard')
def dashboard():
    return authenticate_dashboard()


@app.route('/dashboard/verspringen', methods=['GET', 'POST'])
def vertesprong():
    return render_templates.vertesprong()


@app.route('/dashboard/sprint', methods=['GET', 'POST'])
def sprinten():
    return render_templates.sprinten()


@app.route('/dashboard/zijwaartsspringen', methods=['GET', 'POST'])
def zijwaarts_springen():
    return render_templates.zijwaarts_springen()


@app.route('/dashboard/handoogcoordinatie', methods=['GET', 'POST'])
def hand_oog_coordinatie():
    return render_templates.hand_oog_coordinatie()


@app.route('/dashboard/evenwichtsbalk', methods=['GET', 'POST'])
def evenwichtsbalk():
    return render_templates.evenwichtsbalk()


@app.route('/dashboard/zijwaartsverplaatsen', methods=['GET', 'POST'])
def zijwaarts_verplaatsen():
    return render_templates.zijwaarts_verplaatsen()


@app.route('/dashboard/cod', methods=['GET', 'POST'])
def change_of_direction():
    return render_templates.change_of_direction()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
