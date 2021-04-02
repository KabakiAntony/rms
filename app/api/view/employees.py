import os
from app.api import rms
from werkzeug.utils import secure_filename
from flask import request, abort
import psycopg2
from app.api.utils import allowed_extension, custom_make_response,\
     token_required, rename_file, add_id_and_company_id,\
     convert_to_csv, insert_csv


KEY = os.environ.get('SECRET_KEY')
EMPLOYEE_UPLOAD_FOLDER = os.environ.get('EMPLOYEES_FOLDER') 


@rms.route('/auth/upload/employees', methods=['POST'])
@token_required
def upload_employee_master(user):
    """
    upload the employee master file for a
    given company only the admin can do this
    """
    try:
        receivedFile = request.files['employeeExcelFile']
        if allowed_extension(receivedFile.filename) and receivedFile:
            secureFilename = secure_filename(receivedFile.filename)
            filePath = os.path.join(EMPLOYEE_UPLOAD_FOLDER, secureFilename)
            receivedFile.save(filePath)
            new_file_path = rename_file(
                filePath,
                user['companyId'],
                EMPLOYEE_UPLOAD_FOLDER,
                '_employees_'
            )
            add_id_and_company_id(new_file_path, user['companyId'])
            updated_file_path = add_id_and_company_id(
                new_file_path, user['companyId']
            )
            csvFile = convert_to_csv(updated_file_path, EMPLOYEE_UPLOAD_FOLDER)
            insert_csv(csvFile, 'public."Employees"')
            return custom_make_response(
                "data",
                "Employees data saved successfully.",
                200
                )
        else:
            return custom_make_response(
                "error",
                "Only excel files are allowed !",
                400
            )
    except psycopg2.Error as e:
        # exceptions go to site administrator and email
        # the user gets a friendly error notification
        if e.pgcode == ('23505'):
            abort(
                custom_make_response(
                    "error",
                    "The record(s) you are trying to upload already exist in the database !",
                    400
                )
            )
        elif e.pgcode == ('22P04'):
            abort(
                custom_make_response(
                    "error",
                    "The file you are uploading is not in the allowed format !",
                    400
                    )
                )
        else:
            abort(
                custom_make_response(
                    "error",
                    f'The following error occured {e}',
                    400
                    )
                )


        