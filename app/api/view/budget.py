import os
import csv
import psycopg2
from app.api import rms
from app.api.model import db
from werkzeug.utils import secure_filename
from app.api.model.budget import Budget, budget_schema,\
    budgets_schema
from app.api.model.project import Project, project_schema
from flask import request, abort
from app.api.utils import allowed_extension, custom_make_response,\
     token_required, rename_file, add_id_and_company_id,\
     insert_csv, convert_to_csv, generate_db_ids, check_for_whitespace
from .files import insert_file_data, file_operation


# getting environment variables
KEY = os.environ.get('SECRET_KEY')
BUDGET_UPLOAD_FOLDER = os.environ.get('BUDGET_FOLDER')


@rms.route('/auth/upload/budget', methods=['POST'])
@token_required
def upload_budget(user):
    """
    upload  a budget for a given project
    only the creator can upload a budget
    """
    if (user['role'] != "Creator"):
        abort(custom_make_response(
            "error",
            "You are not authorized to carry out this action.",
            403
        ))
    try:
        receivedFile = request.files['budgetExcelFile']
        if allowed_extension(receivedFile.filename) and receivedFile:
            return file_operation(receivedFile,BUDGET_UPLOAD_FOLDER,'Budget',user['companyId'],user['id'])
        return custom_make_response(
            "error",
            "Only excel files are allowed, please select a budget excel file & try again.",
            400
        )

    except Exception as e:
        db.session.rollback()
        # exceptions go to site administrator and email
        # the user gets a friendly error notification
        message = str(e)
        if('InvalidTextRepresentation' in message):
            abort(
                custom_make_response(
                    "error",
                    "The file you are uploading is not in the allowed format\
                         for a budget file, please check and try again.",
                    400
                )
            )
        elif('id' in message):
            abort(
                custom_make_response(
                    "error",
                    "Please select the project you are uploading a budget for.",
                    400
                )
            )
        else:
            abort(
                custom_make_response(
                    "error",
                    f"The following error occured :: {message}",
                    400
                )
            )
    



    

    

