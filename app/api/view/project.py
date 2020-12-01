import os
import jwt
from app.api import rms
from app.api.model import db
from app.api.model.project import Project, project_schema,\
    projects_schema
from app.api.model.user import User, user_schema
from flask import request, abort
from app.api.utils import check_for_whitespace, custom_make_response


# getting environment variables
KEY = os.environ.get('SECRET_KEY')


@rms.route('/auth/projects', methods=['POST'])
def create_new_project():
    """
    create new project
    only the admin can create projects
    """
    auth_token = request.cookies.get('auth_token')
    if not auth_token:
        abort(
            custom_make_response(
                "error",
                "A required piece of authorization seems to be missing!",
                401
            )
        )
    auth_data = jwt.decode(auth_token, KEY, algorithm="HS256")
    if (auth_data['role'] != 'Admin'):
        abort(
            custom_make_response(
                "error",
                "It seems you are not authorized to create new projects!",
                401
            )
        )
    try:
        data = request.get_json()
        current_user = User.query.\
            filter_by(username=auth_data['username']).first()
        _data = user_schema.dump(current_user)
        projectName = data['project_name']
        companyId = _data['companyId']
        dateFrom = data['date_from']
        dateTo = data['date_to']
    except Exception as e:
        abort(
            custom_make_response(
                "error",
                f"{e} One or more mandatory fields has not been filled!", 400)
        )
    check_for_whitespace(data, [
        'project_name',
        'companyId',
        'dateFrom',
        'dateTo'
    ])
    if Project.query.filter_by(project_name=data['project_name']).first():
        abort(
            custom_make_response(
                "error",
                "There is a conflict in project name, change & try again.",
                409
            )
        )
    new_project = Project(
        project_name=projectName,
        companyId=companyId,
        date_from=dateFrom,
        date_to=dateTo
    )
    db.session.add(new_project)
    db.session.commit()
    return custom_make_response(
        "data",
        f" {projectName} created successfully.",
        201
    )
