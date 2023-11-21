from db import db

class TopicModel(db.Model):
    __tablename__ = "topics"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), unique = False, nullable= False)
    project = db.relationship("ProjectModel", back_populates = "topics")
    messages = db.relationship("MessageModel", back_populates = "topic", lazy = "select")


