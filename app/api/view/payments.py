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
from .files import insert_file_data, file_operation,error_messages


# getting environment variables
KEY = os.environ.get('SECRET_KEY')
PAYMENTS_UPLOAD_FOLDER = os.environ.get('PAYMENTS_FOLDER')


@rms.route('/auth/upload/payments', methods=['POST'])
@token_required
def upload_payment(user):
    """
    upload  a payment for a given project
    only the creator can upload a payment
    """
    if (user['role'] != "Creator"):
        abort(custom_make_response(
            "error",
            "You are not authorized to carry out this action!",
            403
        ))
    try:
        receivedFile = request.files['paymentExcelFile']
        if allowed_extension(receivedFile.filename) and receivedFile:
            return file_operation(receivedFile,PAYMENTS_UPLOAD_FOLDER,'Payment',user['companyId'],user['id'])
        return custom_make_response(
            "error",
            "Only excel files are allowed, please select a budget excel file & try again.",
            400
        )
    except Exception as e:
        error_messages(e,"payment")