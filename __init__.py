from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    
    @app.route("/")
    def home():
        return render_template("index.html")

    return app

create_app()