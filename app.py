from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from api import fetch_rate
from models import db, Rate
from email.utils import parsedate_to_datetime

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    @app.route("/")
    def home():
        return render_template("index.html")
    
    @app.route("/api/rates/<base>/<target>")
    def get_rates(base=None, target=None):
        data = fetch_rate(base, target)
        date = parsedate_to_datetime(data["time"]).date()
        Rate.add_rate(date, data["rate"])
        return jsonify({"date": str(date), "rate": data["rate"]})
    
    @app.route("/api/rates/db")
    def get_db():
        rates = Rate.query.all()
        return jsonify([{"date": str(rate.date), "rate": rate.rate, "is_lowest": rate.is_lowest} for rate in rates])

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()