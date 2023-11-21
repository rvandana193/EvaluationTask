import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import MessageModel
from schemas import MessageSchema, MessageUpdateSchema

blp = Blueprint("Messages", __name__, description="Operation on messsages")

@blp.route("/message/<string:message_id>")
class Message(MethodView):
    @blp.response(200, MessageSchema)
    def get(self, message_id):
       message = MessageModel.query.get_or_404(message_id)
       return message

    def delete(self, message_id):
        message = MessageModel.query.get_or_404(message_id)
        db.session.delete(message)
        db.session.commit()
        return {"message":"Message deleted."}

    @blp.arguments(MessageUpdateSchema)
    @blp.response(200, MessageSchema)
    def put(self, message_data, message_id):

        message = MessageModel.query.get(message_id)

        if message:
            message.name = message_data["name"]

        else: 
            message = MessageModel(id= message_id, **message_data)

        db.session.add(message)
        db.session.commit()

        return message
        

@blp.route("/message")
class MessageList(MethodView):
    @blp.response(200,MessageSchema(many=True))
    def get(self):
        return MessageModel.query.all()

    @blp.arguments(MessageSchema)
    @blp.response(201,MessageSchema)
    def post(self, message_data):
        message = MessageModel(**message_data)

        try:
            db.session.add(message)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the message.")
        
        return message