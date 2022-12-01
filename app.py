import flask
from flask import Flask, render_template
from authentication.authentication import authenticate_dashboard, handle_logout, handle_login, handle_request
import render_templates

def init_app():
    app = Flask(__name__)

    with app.app_context():
        from visualisation.dashboard_template import init_dashboard_template
        app = init_dashboard_template(app)
        return app

app = init_app()
app.secret_key = 'databaseproject'


@app.route('/')
def intro():
    return render_template('intro.html')


@app.route('/request', methods=['GET', 'POST'])
def request():
    return handle_request()


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
def sprint():
    return render_templates.sprint()


@app.route('/dashboard/cod', methods=['GET', 'POST'])
def change_of_direction():
    return render_templates.change_of_direction()


@app.route('/dashboard/algemene_motoriek', methods=['GET', 'POST'])
def algemene_motoriek():
    return render_templates.algemene_motoriek()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
