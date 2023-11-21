from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique = True, nullable=False)
    phn_no = db.Column(db.String(10), nullable = False)
    projects = db.relationship("ProjectModel",back_populates = "user", lazy = "dynamic")
