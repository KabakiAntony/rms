import os
import jwt
from app.api import rms
from app.api.model import db
from app.api.model.project import Project, project_schema,\
    projects_schema
from app.api.model.user import User, user_schema
from flask import request, abort
from app.api.utils import check_for_whitespace, custom_make_response,\
    generate_db_ids, token_required


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
                """
                Authorization cookies for this action seem to be missing,
                please login and try again, if the problem persists , 
                contact site administrator.
                """,
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
        # change from username to id
        current_user = User.query.\
            filter_by(id=auth_data['id']).first()
        _data = user_schema.dump(current_user)
        companyId = _data['companyId']
        projectName = data['project_name'] + '.' + companyId
        dateFrom = data['date_from']
        dateTo = data['date_to']
        id = generate_db_ids()
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
    if Project.query.filter_by(project_name=projectName).first():
        abort(
            custom_make_response(
                "error",
                """
                You already have another project in that name,
                Please change and try again !
                """,
                409
            )
        )
    new_project = Project(
        id=id,
        project_name=projectName,
        companyId=companyId,
        date_from=dateFrom,
        date_to=dateTo
    )
    db.session.add(new_project)
    db.session.commit()
    return custom_make_response(
        "data",
        f"Project {projectName.split('.', 1)[0]} created successfully.",
        201
    )


@rms.route('/projects/<companyId>')
@token_required
def get_projects(user, companyId):
    """ get projects for the given user company"""
    company_projects = Project.query\
        .filter_by(companyId=companyId).all()
    return custom_make_response(
        "data",
        projects_schema.dump(company_projects),
        200
    )
