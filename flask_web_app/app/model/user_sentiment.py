# file berisi representasi table user_sentimen dari database dalam bentuk model
from app import db
from datetime import datetime

class UserSentimen(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review = db.Column(db.String(1052))
    sentiment = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<UserSentimen {}>'.format(self.id)