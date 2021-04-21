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

    insert_file_data(company_id, _amount,file_src,renamed_file_path,user_id)

    return custom_make_response(
        "data",
        f"{file_src} file uploaded successfully and sent for authorization.",
        200
    )
    

def insert_file_data(company_id, file_amt, file_typ,file_url,created_by):
    """ given an excel file after it has gone
    under all conversions the prepare all the 
    details and insert them into the files table.
    """
    project_name = request.form['projectName']
    projectName = project_name + '.' + company_id
    this_project = Project.query.\
        filter_by(project_name=projectName).first()
    project = project_schema.dump(this_project)
    project_id = project['id']
    id = generate_db_ids()
    date_created = datetime.datetime.utcnow()
    todays_date = date_created.strftime('%Y-%m-%d')
    file_status = "Pending"

    new_file = Files(
        id=id,
        companyId=company_id,
        projectId=project_id,
        fileType=file_typ,
        # fileVersion=file_ver,
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

# def check_if_file_exists_and_status(project_id, file_amount):
#     """
#     given a file check if the file is still in pending
#     status , compare the project id and amount of files 
#     already uploaded and the status if the status is pending
#     then don't allow for the file to be uploaded again 
#     but if the status if rejected then you can upload the file again
#     but if the file has been approved then it means the project has already
#     been paid for so also don't allow for upload again so
#     we return the status to notify the user 
#     that is approved then already paid for so we are not paying again
#     pending wait for the authorizer to reject or authorize the file so 
#     we also can upload the file again but if the return is rejected then we 
#     can always upload the file again.
#     if there is no file in the db that meets any of the above requirements 
#     then go ahead and upload so the return is none
#     """


    
