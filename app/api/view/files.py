import os
import csv
import datetime
from app.api import rms
from app.api.model import db
from flask import request, abort, send_from_directory, current_app
from app.api.utils import generate_db_ids
from app.api.model.project import Project, project_schema
from app.api.model.files import Files, file_schema, files_schema
from werkzeug.utils import secure_filename
from app.api.utils import rename_file, convert_to_csv, custom_make_response, \
    token_required, get_file_name, remove_unused_duplicates


DB_URL = os.environ.get("DATABASE_URL")
PAYMENTS_UPLOAD_FOLDER = os.environ.get("PAYMENTS_FOLDER")
BUDGET_UPLOAD_FOLDER = os.environ.get("BUDGET_FOLDER")


def file_operation(received_file, upload_folder, file_src, company_id, user_id):
    """
    takes a file from payments/budget uploads ,
    convert the file to a csv , extract an amount
    """
    secureFilename = secure_filename(received_file.filename)
    filePath = os.path.join(
        current_app.root_path, upload_folder, secureFilename)
    received_file.save(filePath)
    renamed_file_path = rename_file(
        filePath,
        company_id,
        upload_folder,
        "_" + request.form["projectName"] + "_" + file_src + "_",
    )
    print(renamed_file_path)
    csvFile = convert_to_csv(renamed_file_path, upload_folder)
    if file_src == "Budget":
        _amount = get_budget_amount(csvFile, renamed_file_path)
        if check_pending_files(company_id, file_src, _amount):
            remove_unused_duplicates(csvFile)
            remove_unused_duplicates(renamed_file_path)
            abort(409, "File Pending")
    else:
        _amount = get_payment_amount(csvFile, renamed_file_path)
        if check_pending_files(company_id, file_src, _amount):
            remove_unused_duplicates(csvFile)
            remove_unused_duplicates(renamed_file_path)
            abort(409, "File Pending")

        budget_file = get_project_file(company_id, "Budget")
        if not budget_file:
            remove_unused_duplicates(csvFile)
            remove_unused_duplicates(renamed_file_path)
            abort(404, "No Budget For Project")

        budget_amount = budget_file["fileAmount"]
        if budget_amount < float(_amount):
            remove_unused_duplicates(csvFile)
            remove_unused_duplicates(renamed_file_path)
            abort(400, "Project Amount Greater Than")

        status = budget_file["fileStatus"]
        if not (status == "Authorized"):
            remove_unused_duplicates(csvFile)
            remove_unused_duplicates(renamed_file_path)
            abort(400, "Budget  Unauthorized")

    renamed_file = get_file_name(renamed_file_path)
    insert_file_data(company_id, _amount, file_src, renamed_file, user_id)
    return custom_make_response(
        "data", f"{file_src} file successfully sent for authorization.", 200
    )


def get_project_id(company_id):
    """get the projectId for use in various functions"""
    project_name = request.form["projectName"]
    projectName = project_name + "." + company_id
    this_project = Project.query.filter_by(project_name=projectName).first()
    project = project_schema.dump(this_project)
    return project["id"]


def insert_file_data(company_id, file_amt, file_typ, file_name, created_by):
    """given an excel file after it has gone
    under all conversions the prepare all the
    details and insert them into the files table.
    """
    project_id = get_project_id(company_id)
    id = generate_db_ids()
    date_created = datetime.datetime.utcnow()
    todays_date = date_created.strftime("%Y-%m-%d")
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
        fileName=file_name,
    )
    # insert the data into the db
    db.session.add(new_file)
    db.session.commit()


def get_payment_amount(payment_csv_file, renamed_file):
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
    if not payment_amount:
        remove_unused_duplicates(payment_csv_file)
        remove_unused_duplicates(renamed_file)
        abort(400, "Wrong file format")
    return payment_amount


def get_budget_amount(budget_file_csv, renamed_file):
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
    if not budget_amount:
        remove_unused_duplicates(budget_file_csv)
        remove_unused_duplicates(renamed_file)
        abort(400, "Wrong file format")
    return budget_amount


def get_project_file(company_id, file_type):
    project_id = get_project_id(company_id)
    the_file = (
        Files.query.filter_by(projectId=project_id)
        .filter_by(fileType=file_type)
        .first()
    )
    _file = file_schema.dump(the_file)
    return _file


def check_pending_files(company_id, file_type, amount):
    project_id = get_project_id(company_id)
    the_file = (
        Files.query.filter_by(projectId=project_id)
        .filter_by(fileType=file_type)
        .filter_by(fileAmount=amount)
        .filter_by(fileStatus="Pending")
        .first()
    )
    _file = file_schema.dump(the_file)
    return _file


def error_messages(msg, file_src):
    """cascade the error to the correct code"""
    db.session.rollback()
    message = str(msg)
    if "InvalidTextRepresentation" in message\
       or "list index out of range" in message\
       or "Wrong file format" in message:
        abort(
            custom_make_response(
                "error",
                f"The file you are uploading is not in \
                        the allowed format for a {file_src} file,\
                            please check & try again.",
                400,
            )
        )
    elif "id" in message:
        abort(
            custom_make_response(
                "error",
                f"Please select the project \
                        you are uploading a {file_src} file for.",
                400,
            )
        )
    elif "File Pending" in message:
        abort(
            custom_make_response(
                "error",
                f"A {file_src} file with similar info is available\
                         & marked as pending in the system,\
                              kindly ask your authorizer to act on it.",
                409,
            )
        )
    elif "No Budget For Project" in message:
        abort(
            custom_make_response(
                "error",
                "A budget was not found for this project please upload\
                        one for authorization before proceeding.",
                404,
            )
        )
    elif "Budget  Unauthorized" in message:
        abort(
            custom_make_response(
                "error",
                "The budget for this project has not been authorized,\
                        Kindly ask the authorizer to act on it.",
                400,
            )
        )

    elif "Project Amount Greater Than" in message:
        abort(
            custom_make_response(
                "error",
                "The payment file amount exceeds the budget for this project,\
                        please review your file & try again.",
                400,
            )
        )
    else:
        abort(
            custom_make_response(
                "error", f"The following error occured :: {message}", 400
            )
        )


@rms.route('/files/<companyId>/<projectName>', methods=["GET"])
@token_required
def get_company_files(user, companyId, projectName):
    """return the files for a given company"""

    project_name = projectName + "." + companyId
    this_project = Project.query.filter_by(project_name=project_name).first()
    project = project_schema.dump(this_project)

    the_files = Files.query.filter_by(companyId=user['companyId']).\
        filter_by(projectId=project['id']).all()

    _the_files = files_schema.dump(the_files)
    if not _the_files:
        return abort(
            custom_make_response(
                "error",
                "No file(s) have been found for the selected \
                    project,upload some & try again.",
                404
            )
        )
    return custom_make_response(
        "data", _the_files, 200
    )


@rms.route('/auth/files/<companyId>/<fileType>', methods=["GET"])
@token_required
def get_authorizer_files(user, companyId, fileType):
    """return the files for a given company for the authorizer"""
    file_data = db.session.query(Files, Project).\
        filter(Files.projectId == Project.id).\
        filter_by(fileType=fileType.capitalize()).all()

    if not file_data:
        abort(
            custom_make_response(
                "error",
                f"No {fileType} file(s) have been found for your company,\
                     ask the creator to upload & try again.", 404
            )
        )

    fileList = []
    for result in file_data:
        result_format = {
            "fileType": result[0].fileType,
            "project_name": result[1].project_name,
            "fileStatus": result[0].fileStatus,
            "fileAmount": result[0].fileAmount,
            "dateCreated": result[0].dateCreated.strftime('%m-%d-%Y'),
            "fileName": result[0].fileName
        }
        fileList.append(result_format)

    return custom_make_response("data", fileList, 200)


@rms.route('/uploads/<path:fileType>/<path:fileName>', methods=['GET'])
@token_required
def download(user, fileType, fileName):
    downloaded_file = ""
    if fileType == "budget":
        downloaded_file = send_from_directory(
            BUDGET_UPLOAD_FOLDER, fileName, as_attachment=True)
    else:
        downloaded_file = send_from_directory(
            PAYMENTS_UPLOAD_FOLDER, fileName, as_attachment=True)
    return downloaded_file
