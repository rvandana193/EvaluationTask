from db import db

class MessageModel(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80),unique = False, nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), unique = False, nullable= False)
    topic = db.relationship("TopicModel", back_populates = "messages")
   

