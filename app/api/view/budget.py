import os
from app.api import rms
from app.api.model import db
import csv
from werkzeug.utils import secure_filename
from app.api.model.budget import Budget, budget_schema,\
    budgets_schema
from app.api.model.project import Project, project_schema
from flask import request, abort
from app.api.utils import allowed_extension, custom_make_response,\
     token_required, rename_file, add_id_and_company_id,\
     insert_csv, convert_to_csv, generate_db_ids, check_for_whitespace


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
            "You are not authorized to carry out this action!",
            403
        ))
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
            budget_amount = get_budget_amount(csvFile)
            insert_budget_data(user['companyId'], budget_amount, new_file_path)
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
        print(f"{e}")
        # exceptions go to site administrator and email
        # the user gets a friendly error notification
        abort(
            custom_make_response(
                "error",
                f"The following error occured : '{e}'",
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
    count_rows = 0
    for row in reader_file:
        count_rows += 1
    budget_amount = row[1]
    return budget_amount


def insert_budget_data(company_id, budgetAmt, fileUrl):
    """
    insert budget data into the budget
    table for the authorizer
    to act accordingly
    """
    try:
        project_name = request.form['projectName']
        projectName = project_name + '.' + company_id
        this_project = Project.query.\
            filter_by(project_name=projectName).first()
        project = project_schema.dump(this_project)
        project_id = project['id']
        id = generate_db_ids()
        companyId = company_id
        amount = budgetAmt
        fileUrl = fileUrl

        new_budget = Budget(
            id=id,
            companyId=companyId,
            projectId=project_id,
            amount=amount,
            fileUrl=fileUrl
            )
        # insert the data into the db
        db.session.add(new_budget)
        db.session.commit()
    except Exception as e:
        abort(
            custom_make_response(
                "error",
                f"An error occured saving budget data {e}",
               400 
            )
        )
    

