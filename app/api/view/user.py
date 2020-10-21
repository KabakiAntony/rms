"""
various user views will be handled here
"""
import os
import jwt
import datetime
from app.api import rms
from app.api.model.models import db
from app.api.model.user import user_schema, users_schema, User
from app.api.model.company import Company, company_schema
from flask import request, abort, render_template
from app.api.utils import check_for_whitespace, isValidEmail,\
     send_mail, custom_make_response, company_token_required,\
     isValidPassword


# get environment variables
KEY = os.getenv('SECRET_KEY')
signup_url = os.getenv('SIGNUP_URL')
verification_url = os.getenv('VERIFY_EMAIL_URL')
password_reset_url = os.getenv('PASSWORD_RESET_URL')


@rms.route('/auth/admin/signup', methods=['POST'])
def signup_admin_user():
    """
    this method creates a company users admin
    admin user does not need to verify their
    email since they already got here by way
    of email.
    """
    try:
        admin_data = request.get_json()
        # we have to get the company id
        # as we only get the company name
        # from the UI
        this_company = Company.query\
            .filter_by(company=admin_data['company']).first()
        _company = company_schema.dump(this_company)
        companyId = _company['id']
        firstname = admin_data['firstname']
        email = admin_data['email']
        password = admin_data['password']
    except Exception as e:
        abort(
            custom_make_response(
                "error",
                f"{e} One or more mandatory fields has not been filled!", 400)
        )
    # check data for sanity incase it bypass js on the frontend
    check_for_whitespace(
        admin_data,
        ['companyId', 'firstname', 'email', 'password']
    )
    isValidEmail(email)
    # check if user is already registered
    if User.query.filter_by(email=admin_data['email']).first():
        abort(
            custom_make_response(
                "error",
                "The user is already registered please use another email!", 409
            )
        )
    isValidPassword(password)
    new_admin_user = User(
        firstname=firstname,
        email=email,
        password=password,
        companyId=companyId,
        role="Admin",
        isActive="True"
    )
    db.session.add(new_admin_user)
    db.session.commit()
    return custom_make_response(
        "data",
        user_schema.dump(new_admin_user),
        200
    )


# this route is accessible to the admin
# when they are logged in
@rms.route('/auth/admin/create', methods=['POST'])
def create_other_users():
    """
    here the admin creates the other
    system users.
    """
    try:
        user_data = request.get_json()
        companyId = user_data['companyId']
        firstname = user_data['firstname']
        email = user_data['email']
        password = user_data['password']
        role = user_data['role']
    except Exception as e:
        abort(
            custom_make_response(
                "error",
                f"{e} One or more mandatory fields has not been filled!", 400)
        )
    # check data for sanity incase it bypass js on the frontend
    check_for_whitespace(
        user_data,
        ['companyId', 'firstname', 'email', 'password', 'role', 'isActive']
    )
    isValidEmail(email)
    # check if user is already registered
    if User.query.filter_by(email=user_data['email']).first():
        abort(
            custom_make_response(
                "error",
                "The user is already a system user please register another.",
                409
            )
        )
    isValidPassword(password)
    new_user = User(
        firstname=firstname,
        email=email,
        password=password,
        companyId=companyId,
        role=role,
        isActive="True"
    )
    db.session.add(new_user)
    db.session.commit()
    return custom_make_response(
        "data",
        user_schema.dump(new_user),
        200
    )


@rms.route('/admin/fe/signup', methods=['GET'])
@company_token_required
def load_signup_ui(company):
    """
    load the ui user for admin signup
    """
    _company = company['company']
    return render_template(
        'signup.html',
        title="Sign Up",
        company=_company,
    )
