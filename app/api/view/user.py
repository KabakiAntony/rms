"""
various user views will be handled here
"""
import os
import jwt
import datetime
from app.api import rms
from app.api.model.models import db
from app.api.model.user import user_schema, users_schema, User
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
    we handle admin user sign up here
    for the admin user since they
    recieved the email then it means
    them being here on the signup page
    that their email is true
    hence no need to activate their account
    but the users they create after that
    have to activate their account.
    """
    try:
        user_data = request.get_json()
        companyId = user_data['companyId']
        firstname = user_data['firstname']
        email = user_data['email']
        password = user_data['password']
    except Exception as e:
        abort(
            custom_make_response(
                "error",
                f"{e}One or more mandatory fields has not been filled!", 400)
        )
    # check data for sanity incase it bypass js on the frontend
    check_for_whitespace(user_data, ['companyId', 'firstname', 'email', 'password'])
    isValidEmail(email)
    # check if user is already registered
    if User.query.filter_by(email=user_data['email']).first():
        abort(
            custom_make_response(
                "error",
                "That email is already in use, please choose another one", 409
            )
        )
    isValidPassword(password)
    new_user = User(
        firstname=firstname,
        email=email,
        password=password,
        companyId=companyId,
        role="Admin",
        isActive="True"
    )
    db.session.add(new_user)
    db.session.commit()
    return custom_make_response(
        "data",
        user_schema.dump(new_user),
        200
    )


@rms.route('/fe/signup', methods=['GET'])
@company_token_required
def load_signup_ui(company):
    """
    load the user for user signup
    """
    _company = company['company']
    return render_template('signup.html', title='Sign Up', company=_company)


@rms.route('/auth/other/create', methods=['POST'])
def signup_other_users():
    """
    here the admin creates the other 
    system users.
    """
