import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import ProjectModel, TopicModel, MessageModel
from schemas import ProjectSchema, ProjectUpdateSchema
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import joinedload

blp = Blueprint("Projects", __name__, description="Operation on projects")

@blp.route("/project/<string:project_id>")
class Project(MethodView):
    @blp.response(200, ProjectSchema)
    def get(self, project_id):
       project = ProjectModel.query.get_or_404(project_id)
       return project

    def delete(self, project_id):
        project = ProjectModel.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return {"message":"Project deleted."}

    @blp.arguments(ProjectUpdateSchema)
    @blp.response(200, ProjectSchema)
    def put(self, project_data, project_id):

        project = ProjectModel.query.get(project_id)

        if project:
            project.name = project_data["name"]

        else: 
            project = ProjectModel(id= project_id, **project_data)

        db.session.add(project)
        db.session.commit()

        return project
        

@blp.route("/project")
class ProjectList(MethodView):
    @blp.response(200,ProjectSchema(many=True))
    def get(self):
        projects = (
            db.session.query(ProjectModel)
            .options(
                db.joinedload(ProjectModel.topics)
                .joinedload(TopicModel.messages)
            )
            .all()
        )

        
        print("project: ", projects)
       
        if not projects:
            abort(404, message="Project not found")

        return projects
        

    @blp.arguments(ProjectSchema)
    @blp.response(201,ProjectSchema)
    def post(self, project_data):
        project = ProjectModel(**project_data)

        try:
            db.session.add(project)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the project.")
        
        return project