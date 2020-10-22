"""
various user views will be handled here
"""
import os
import jwt
import datetime
from app.api import rms
from app.api.model.models import db
from flask import request, abort, url_for, redirect
from app.api.model.user import user_schema, users_schema, User
from app.api.model.company import Company, company_schema
from flask_login import current_user, login_user, logout_user,\
    login_required
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
        201
    )


# this route is accessible to the admin
# when they are logged in
@rms.route('/auth/admin/create', methods=['POST'])
@login_required
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
        201
    )


@rms.route('/auth/signin', methods=['POST'])
def signin_all_users():
    """
    this signs in all users
    """
    if current_user.is_authenticated:
        return redirect(url_for('rms.load_welcome_ui'))
    try:
        user_data = request.get_json()
        email = user_data['email']
        password = user_data['password']
    except Exception as e:
        abort(custom_make_response(
            "error",
            f"{e} one or more mandatory fields was not filled!",
            400
        ))
    # check data for sanity incase it bypass js on the frontend
    check_for_whitespace(user_data, ['email', 'password'])
    isValidEmail(email)
    # check if user is already registered
    user = User.query.filter_by(email=user_data['email']).first()
    if not user:
        abort(
            custom_make_response(
                "error",
                "the user has not been found, please sign up to use system!",
                404
            )
        )
    _user = user_schema.dump(user)
    print(_user)
    _password_hash = _user['password']
    if not User.compare_password(_password_hash, password):
        abort(
            custom_make_response(
                "error",
                "Invalid email and or password, please check and try again!",
                401
            )
        )
    login_user(user, remember=user_data)
    return custom_make_response(
        "data",
        "login successful",
        200
    )
