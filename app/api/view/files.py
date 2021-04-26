import os
import csv
import datetime
from app.api.model import db
from flask import request, abort
from app.api.utils import generate_db_ids
from app.api.model.project import Project, project_schema
from app.api.model.files import Files,file_schema
from werkzeug.utils import secure_filename
from app.api.model.budget import Budget, budget_schema,\
    budgets_schema
from flask import request, abort
from app.api.utils import allowed_extension, custom_make_response,\
     token_required, rename_file, add_id_and_company_id,\
     insert_csv, convert_to_csv, generate_db_ids, check_for_whitespace


def file_operation(received_file,upload_folder,file_src,company_id,user_id):
    """
    takes a file from payments/budget uploads ,
    convert the file to a csv , extract an amount
    """
    secureFilename = secure_filename(received_file.filename)
    filePath = os.path.join(upload_folder, secureFilename)
    received_file.save(filePath)
    renamed_file_path = rename_file(
        filePath,
        company_id,
        upload_folder,
        '_'+request.form['projectName'] +'_'+file_src+'_'
    )
    csvFile = convert_to_csv(renamed_file_path, upload_folder)
    if(file_src == 'Budget'):
        _amount = get_budget_amount(csvFile)
    else:
        _amount = get_payment_amount(csvFile)

        budget_file = get_project_file(company_id, "Budget")
        if not budget_file:
            remove_unused_duplicates(csvFile)
            remove_unused_duplicates(renamed_file_path)
            abort(404,"No Budget For Project")

        budget_amount = budget_file['fileAmount']
        if (budget_amount < float(_amount)):
            remove_unused_duplicates(csvFile)
            remove_unused_duplicates(renamed_file_path)
            abort(400,"Project Amount Greater Than")
        
        status = budget_file['fileStatus']
        if not (status == "Authorized"):
            remove_unused_duplicates(csvFile)
            remove_unused_duplicates(renamed_file_path)
            abort(400,"Budget  Unauthorized")
  
    # check if file is pending
    project_file = get_project_file(company_id, file_src)
    if project_file and project_file['fileStatus'] == "Pending":
        remove_unused_duplicates(csvFile)
        remove_unused_duplicates(renamed_file_path)
        abort(409,"File Pending")
    
    insert_file_data(company_id, _amount,file_src,renamed_file_path,user_id)
    return custom_make_response(
        "data",
        f"{file_src} file successfully sent for authorization.",
        200)

def get_project_id(company_id):
    """get the projectId for use in various functions"""
    project_name = request.form['projectName']
    projectName = project_name + '.' + company_id
    this_project = Project.query.\
        filter_by(project_name=projectName).first()
    project = project_schema.dump(this_project)
    return project['id']


def insert_file_data(company_id, file_amt, file_typ,file_url,created_by):
    """ given an excel file after it has gone
    under all conversions the prepare all the 
    details and insert them into the files table.
    """
    project_id = get_project_id(company_id)
    id = generate_db_ids()
    date_created = datetime.datetime.utcnow()
    todays_date = date_created.strftime('%Y-%m-%d')
    file_status = "Pending"

    new_file = Files(
        id=id,
        companyId=company_id,
        projectId=project_id,
        fileType=file_typ,
        fileAmount=file_amt,
        createdBy=created_by,
        dateCreated=todays_date,
        authorizedOrRejectedBy=created_by,
        dateAuthorizedOrRejected=todays_date,
        fileStatus=file_status,
        fileUrl=file_url
        )
    # insert the data into the db
    db.session.add(new_file)
    db.session.commit()


def get_payment_amount(payment_csv_file):
    """
    given a payment csv file extract the payment
    amount and return it
    """
    saved_csv = open(payment_csv_file)
    reader_file = csv.reader(saved_csv)
    count_rows = 0
    for row in reader_file:
        count_rows += 1
    payment_amount = row[3]
    return payment_amount


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

def get_project_file(company_id, file_type):
    project_id = get_project_id(company_id)
    the_file = Files.query.\
        filter_by(projectId=project_id).\
            filter_by(fileType=file_type).first()
    _file = file_schema.dump(the_file)
    return _file

def remove_unused_duplicates(file_path):
    """remove unused files from server"""
    os.remove(file_path)

def error_messages(msg,file_src):
    """cascade the error to the correct code"""
    db.session.rollback()
    message = str(msg)
    if('InvalidTextRepresentation' in message \
        or 'list index out of range' in message):
            abort(
                custom_make_response(
                    "error",
                    f"The file you are uploading is not in \
                        the allowed format for a {file_src} file,\
                            please check & try again.",
                    400
                )
            )
    elif('id' in message):
            abort(
                custom_make_response(
                    "error",
                    f"Please select the project \
                        you are uploading a {file_src} file for.",
                    400
                )
            )
    elif('File Pending' in message):
            abort(
                custom_make_response(
                    "error",
                    f"A {file_src} file with similar info is available\
                         & marked as pending in the system,\
                              kindly ask your authorizer to act on it.",
                    409
                )
            )
    elif('No Budget For Project' in message):
            abort(
                custom_make_response(
                    "error",
                    "A budget was not found for this project please upload\
                        one for authorization before proceeding.",
                    404
                )
            )
    elif('Budget  Unauthorized' in message):
            abort(
                custom_make_response(
                    "error",
                    "The budget for this project has not been authorized,\
                        Kindly ask the authorizer to act on it.",
                    400
                )
            )
    
    elif('Project Amount Greater Than' in message):
            abort(
                custom_make_response(
                    "error",
                    "The payment file amount exceeds the budget for this project,\
                        please review your file & try again.",
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
        
   
    




    
