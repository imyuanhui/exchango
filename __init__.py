from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .api import fetch_rate

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db = SQLAlchemy(app)
    
    @app.route("/")
    def home():
        return render_template("index.html")
    
    @app.route("/api/rates/<base>/<target>")
    def get_rates(base=None, target=None):
        return fetch_rate(base, target)

    return app

create_app()