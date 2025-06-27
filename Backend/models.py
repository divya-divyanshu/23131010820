from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class URLMapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String, nullable=False)
    short_code = db.Column(db.String, unique=True, nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)
