from flask import Flask

def init_app():
    app = Flask(__name__)

    with app.app_context():
        from visualisation.algemene_moteriek_dashboard import init_dashboard
        app = init_dashboard(app) 
        return app

app = init_app()

if __name__ == "__main__":
    app.run()