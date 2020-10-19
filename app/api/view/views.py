import os
import jwt
import datetime
from flask import request, abort, render_template, jsonify
from app.api import rms
from app.api.model.models import db, User, Employees, Company,\
    Files, Budget, Project
from app.api.model.models import company_schema, companies_schema
from app.api.utils import check_for_whitespace, isValidEmail,\
    isValidPassword, token_required, send_mail, check_model_return,\
    custom_make_response


# getting environment variables
KEY = os.getenv('SECRET_KEY')
verification_url = os.getenv('VERIFY_EMAIL_URL')
password_reset_url = os.getenv('PASSWORD_RESET_URL')
signup_url = os.getenv('SIGNUP_URL')


@rms.route('/intent', methods=['POST'])
def signup_intent():
    """
    send a sign up link on the email to
    would be customers
    """
    try:
        data = request.get_json()
        firstname = data["firstname"]
        email = data["email"]
        company = data["company"]
    except Exception:
        abort(
            custom_make_response(
                "error", "One or more mandatory fields has not been filled!", 400)
        )
    # check data for sanity
    check_for_whitespace(data, ['firstname', 'email', 'company'])
    isValidEmail(email)
    # check if the company is already registered
    if Company.query.filter_by(company=data['company']).first():
        abort(
            custom_make_response(
                "error", "please check email for further instructions.", 409
            )
        )
    token = jwt.encode(
        {
            "email": email,
            "company": company,
            'exp': datetime.datetime.utcnow() +
            datetime.timedelta(minutes=1800)
        },
        KEY,
        algorithm='HS256'
    )
    # send signup intent email
    subject = f"""Thank you for registering {company}."""
    content = f"""
    Welcome {firstname},
    <br/>
    <br/>
    We are grateful to have you.<br/>
    Please click on sign up below to register your personal
    information to start using the system.Kindly note this 
    link will only be available for three hours.
    <br/>
    <br/>
    <a href="{signup_url}?in={token.decode('utf-8')}">Sign Up</a>
    <br/>
    <br/>
    Regards Antony,<br/>
    RMS Admin.
    """
    send_mail(email, subject, content)
    new_company = Company(company=company, joined_at=datetime.datetime.now())
    print(new_company)
    db.session.add(new_company)
    db.session.commit()
    print(new_company)
    return company_schema.jsonify(new_company)
    # return custom_make_response(
    #     "data", [{
    #         "Company": company,
    #         "email": email,
    #         "message": "Please check your email to complete registration."
    #     }], 200
    # )


# @rms.route('/signup', methods=['POST'])
# def signup_system_users():
#     """
#     this handles registration of the system
#     users for a particular company
#     """
#     try:
#         data = request.get_json()
#         firstname = data["firstname"]
#         email = data["email"]
#         password = data["password"]
#         # company name comes from the user token
#         # but the user registration we need
#         # companyId so after getting company name
#         # we need to pull companyId from the db &
#         # use that to register the user
#         company = data["company"]
#         # companyId = 
#         role = data["role"]
#         isActive = data["isActive"]
#     except Exception:
#         abort(
#             custom_make_response(
#                 "error",
#                 "One or more mandatory fields has not been filled!", 400)
#         )
#     # check data for sanity
#     check_for_whitespace(data, ['firstname', 'email', 'company'])
#     isValidEmail(email)


@rms.route('/companies', methods=['GET'])
def get_companies():
    """
    get all companies that are registered
    at any onetime 
    also test to see whether marshmallow 
    integration works.
    """
    all_companies = Company.query.all()
    print(all_companies)
    return companies_schema.dump(all_companies)
