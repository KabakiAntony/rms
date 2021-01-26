import os
from app.api import rms
import csv
from werkzeug.utils import secure_filename
from app.api.model.budget import Budget, budget_schema,\
    budgets_schema
from flask import request, abort
from openpyxl import load_workbook
from app.api.utils import allowed_extension, custom_make_response,\
     token_required, rename_file, add_id_and_company_id,\
     insert_csv, convert_to_csv, generate_db_ids


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
    try:
        receivedFile = request.files['budgetExcelFile']
        if allowed_extension(receivedFile.filename) and receivedFile:
            secureFilename = secure_filename(receivedFile.filename)
            filePath = os.path.join(BUDGET_UPLOAD_FOLDER, secureFilename)
            receivedFile.save(filePath)
            new_file_path = rename_file(
                filePath,
                user['companyId'],
                BUDGET_UPLOAD_FOLDER,
                '_budget_'
            )
            csvFile = convert_to_csv(new_file_path, BUDGET_UPLOAD_FOLDER)
            get_budget_amount(csvFile)
            return custom_make_response(
                "data",
                "File uploaded successfully.",
                200
                )
        else:
            return custom_make_response(
                "error",
                "Only excel files are allowed !",
                400
            )
    except Exception as e:
        abort(
            custom_make_response(
                "error",
                f"{e}",
                # "An error occured uploading file \
                #     the administrator has been notified.",
                400
            )
        )


def get_budget_amount(budget_file_csv):
    """
    get the budget amount from
    from the just uploaded file
    """
    saved_csv = open(budget_file_csv, "r")
    reader_file = csv.reader(saved_csv)
    # csv_rows = len(list(reader_file))
    # print(csv_rows[1])
    for row in reader_file:
        print(row[1])


