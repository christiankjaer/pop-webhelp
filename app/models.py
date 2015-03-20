from app import db

class User(db.Model):
    kuid = db.Column(db.String(6), primary_key=True)
