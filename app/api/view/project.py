import os
from app.api import rms
from app.api.model import db
from app.api.model.project import Project, projects_schema
from app.api.model.user import User, user_schema
from flask import request, abort
from app.api.utils import (
    check_for_whitespace,
    custom_make_response,
    generate_db_ids,
    token_required,
)


# getting environment variables
KEY = os.environ.get("SECRET_KEY")


@rms.route("/auth/projects", methods=["POST"])
@token_required
def create_new_project(user):
    """
    create new project
    only the admin can create projects
    """
    try:
        data = request.get_json()
        current_user = User.query.filter_by(id=user["id"]).first()
        _data = user_schema.dump(current_user)
        companyId = _data["companyId"]
        projectName = data["project_name"] + "." + companyId
        dateFrom = data["date_from"]
        dateTo = data["date_to"]
        id = generate_db_ids()
    except Exception as e:
        # exceptions go to site administrator log and email
        # the user gets a friendly error notification
        abort(
            custom_make_response(
                "error",
                f"{e} One or more mandatory fields has not been filled!", 400
            )
        )
    check_for_whitespace(
        data, ["project_name", "companyId", "dateFrom", "dateTo"])
    if Project.query.filter_by(project_name=projectName).first():
        abort(
            custom_make_response(
                "error",
                """
                You already have another project in that name,
                Please change and try again !
                """,
                409,
            )
        )
    new_project = Project(
        id=id,
        project_name=projectName,
        companyId=companyId,
        date_from=dateFrom,
        date_to=dateTo,
        project_status="Active"
    )
    db.session.add(new_project)
    db.session.commit()
    return custom_make_response(
        "data",
        f"Project {projectName.split('.', 1)[0]} created successfully.", 201
    )


@rms.route("/projects/<companyId>")
@token_required
def get_projects(user, companyId):
    """get projects for the given user company"""
    if user["companyId"] == companyId:
        company_projects = Project.query.filter_by(companyId=companyId).all()
        if not company_projects:
            return abort(
                custom_make_response(
                    "error",
                    "No projects exist for your company, Once you\
                        create some they will appear here.",
                    404,
                )
            )
        elif company_projects:
            return custom_make_response(
                "data", projects_schema.dump(company_projects), 200
            )
        else:
            return abort(
                custom_make_response(
                    "error",
                    "Bummer an error occured fetching the records,\
                        please refresh and try again.",
                    500,
                )
            )
    else:
        return abort(
            custom_make_response(
                "error",
                "There appears to be a mismatch in the authorization\
                     data,Please logout, login & try again, if the problem\
                          persists,contact the site administrator.",
                400,
            )
        )


@rms.route("/projects/name/<companyId>")
@token_required
def get_projects_name(user, companyId):
    """
    return the project names of a given
    company's project
    """
    company_projects = (
        Project.query.with_entities(Project.project_name)
        .filter_by(companyId=companyId)
        .all()
    )
    project_name = projects_schema.dump(company_projects)
    return custom_make_response("data", project_name, 200)
