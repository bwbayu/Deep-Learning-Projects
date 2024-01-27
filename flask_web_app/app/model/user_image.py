# file berisi representasi table user_image dari database dalam bentuk model
from app import db
from datetime import datetime

class UserImage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String(100))
    classes = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<UserImage {}>'.format(self.id)