import os
import psycopg2
from app.api import rms
from app.api.model import db
from werkzeug.utils import secure_filename
from flask import request, abort
from app.api.model.company import Company, company_schema
from app.api.utils import allowed_extension, custom_make_response,\
     token_required, rename_file, add_id_and_company_id,\
     convert_to_csv, insert_csv, generate_db_ids,\
         check_for_whitespace, isValidPassword
from app.api.email_utils import isValidEmail
from app.api.model.employees import Employees, employee_schema,\
     employees_schema
from app.api.model.user import User

 
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
                    "The record(s) you are trying to upload\
                        already exist in the database !",
                    409
                )
            )
        elif e.pgcode == ('22P04'):
            abort(
                custom_make_response(
                    "error",
                    "The file you are uploading is not in the\
                        allowed format for employees file!",
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


@rms.route('/employees/<companyId>', methods=['GET'])
@token_required
def  get_employees(user,companyId):
    """
    return the employees of a given company
    """
    if user['companyId'] == companyId:
        company_employees = Employees.query\
            .filter_by(companyId=companyId).all()
        if not company_employees:
            return abort(
                custom_make_response(
                    "error",
                    "No employees have been found for your company !\
                        please upload & try again.",
                    404
                )
            )
        elif company_employees:
            return custom_make_response(
                "data",
                employees_schema.dump(company_employees),
                200
            )
        else:
            return abort(
                custom_make_response(
                    "error",
                    "Bummer an error occured fetching the records,\
                        please refresh and try again.",
                    500
                )
            )

    else:
        return abort(
            custom_make_response(
                "error",
                "There appears to be a mismatch in the authorization\
                     data,Please logout, login and try again, if problem\
                          persists,contact the site administrator.",
                401
            )
        )


@rms.route('/auth/admin/employees',methods=['POST'])
def insert_admin_employee():
    """
    insert admin details to the employee
    table.
    """
    try:
        user_data = request.get_json()
        id = generate_db_ids()
        this_company = Company.query\
                .filter_by(company=user_data['company']).first()
        _company = company_schema.dump(this_company)
        companyId = _company['id']
        firstname = user_data['firstname']
        lastname = user_data['lastname']
        mobile = user_data['mobile']
        email = user_data['email']
        password = user_data['password']
        role = user_data['role']
        isActive = user_data['isActive']

        # check data for sanity incase it bypass js on the frontend
        check_for_whitespace(
            user_data,
            [
                'companyId', 
                'firstname',
                'lastname', 
                'email', 
                'mobile',
                'password',
                'role',
                'isActive'])
            
        isValidEmail(email)

        new_employee = Employees(
            id=id,
            companyId=companyId,
            firstname=firstname,
            lastname=lastname,
            mobile=mobile,
            email=email
            )

        db.session.add(new_employee)
        db.session.commit()
        # once you have created an admin as an employee
        # let create them as user in the system.
        isValidPassword(password)

        new_user = User(
            id=id,
            username = user_data['firstname'] + '.' + id,
            email=email,
            password=password,
            role=role,
            companyId=companyId,
            isActive=isActive)
        
        db.session.add(new_user)
        db.session.commit()

        return custom_make_response(
            "data",
            "Your details have bee saved successfully,\
                please login to start using the system.",
            201
        )
    except Exception as e:
        message = str(e)
        if("UniqueViolation" and "Employees_mobile_key" in message):
            abort(
                custom_make_response(
                    "error",
                    "The mobile number you have entered seems\
                        to have been registered to another user,\
                            please change and try again. ",
                    409
                )
            )
        elif("Employees_email_key" and "UniqueViolation" in message):
            abort(
                custom_make_response(
                    "error",
                    "The email address you have entered seems\
                        to have been registered to another user,\
                            please change and try again. ",
                    409
                    )
                )
        else:
            abort(
                custom_make_response(
                    "error",
                    "Bummer an internal error occured, please reload and try again.",
                    500
                )
            )

# @rms.route('/test/employees/<email>', methods=['GET'])
# def get_single_employee(email):
#     """get a single employee, this
#     route is not used on the front end it is
#     basically made to assist in testing"""
#     _employee = Employees.query\
#         .filter_by(email=email).all()
#     this_employee = employee_schema.dump(_employee)
#     if not this_employee:
#         abort(
#             custom_make_response(
#                 "error",
#                 "No employee bears that email.",
#                 404
#             )
#         )
#     else:
#         return custom_make_response(
#             "data",
#             this_employee,
#             200
#         )


    

    

    