from marshmallow import Schema, fields

class PlainUserSchema(Schema):
    id = fields.Str(dump_only= True)
    name = fields.Str(required= True)
    phn_no = fields.Str(required= True)

class PlainProjectSchema(Schema):
    id = fields.Str(dump_only= True)
    name = fields.Str(required= True) 

class PlainTopicSchema(Schema):
    id = fields.Str(dump_only= True)
    name = fields.Str(required= True) 

class PlainMessageSchema(Schema):
    id = fields.Str(dump_only= True)
    name = fields.Str(required= True) 


class ProjectUpdateSchema(Schema):
    name = fields.Str()
    user_id = fields.Int()

class TopicUpdateSchema(Schema):
    name = fields.Str()
    project_id = fields.Int()

class MessageUpdateSchema(Schema):
    name = fields.Str()
    topic_id = fields.Int()

class ProjectSchema(PlainProjectSchema):
    user_id = fields.Int(required = True, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)
    topics = fields.List(fields.Nested(PlainTopicSchema()),dump_only = True,many = True)
    messages = fields.List(fields.Nested(PlainMessageSchema()),dump_only = True,many = True)

class TopicSchema(PlainTopicSchema):
    project_id = fields.Int(required = True, load_only=True)
    project = fields.Nested(PlainProjectSchema(), dump_only=True)
    messages = fields.List(fields.Nested(PlainMessageSchema()),dump_only = True,many = True)

class MessageSchema(PlainMessageSchema):
    topic_id = fields.Int(required = True, load_only=True)
    topic = fields.Nested(PlainTopicSchema(), dump_only=True)

class UserSchema(PlainUserSchema):
    projects = fields.List(fields.Nested(PlainProjectSchema()),dump_only = True)

    