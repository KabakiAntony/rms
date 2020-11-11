"""
various user views will be handled here
"""
import os
import jwt
import datetime
from app.api import rms
from app.api.model.models import db
from flask import request, abort, url_for, redirect,\
     make_response, session
from app.api.model.user import user_schema, users_schema, User
from app.api.model.company import Company, company_schema
from app.api.utils import check_for_whitespace, isValidEmail,\
     send_mail, custom_make_response, token_required,\
     isValidPassword


# get environment variables
KEY = os.getenv('SECRET_KEY')
signup_url = os.getenv('SIGNUP_URL')
verification_url = os.getenv('VERIFY_EMAIL_URL')
password_reset_url = os.getenv('PASSWORD_RESET_URL')


@rms.route('/admin/signup', methods=['POST'])
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
        username = admin_data['username']
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
        ['companyId', 'username', 'email', 'password']
    )
    isValidEmail(email)
    # check if user is already registered
    if User.query.filter_by(email=admin_data['email']).first():
        abort(
            custom_make_response(
                "error",
                "User exists, please use another email!", 409
            )
        )
    isValidPassword(password)
    new_admin_user = User(
        username=username,
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


@rms.route('/auth/signin', methods=['POST'])
def signin_all_users():
    """
    this signs in all users
    """
    try:
        user_data = request.get_json()
        email = user_data['email']
        password = user_data['password']
    except Exception as e:
        abort(custom_make_response(
            "error",
            f"{e} One or more mandatory fields was not filled!",
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
                "User not found, Please sign up to use system!",
                404
            )
        )
    _user = user_schema.dump(user)
    _password_hash = _user['password']
    if not User.compare_password(_password_hash, password):
        abort(
            custom_make_response(
                "error",
                "Incorrect email and or password!",
                401
            )
        )
    # login_user(user, remember=user_data)
    _curr_user = user_schema.dump(user)
    # return redirect(
    #         url_for("rms.load_profile_ui")
    #     )
    token = jwt.encode(
        {
            "username": _curr_user['username'],
            "role": _curr_user['role'],
            'exp': datetime.datetime.now() +
            datetime.timedelta(minutes=480)
        },
        KEY,
        algorithm='HS256'
    )
    # this creates a session for the user in the
    # server so as to help us login and log out
    session['username'] = _curr_user['username']
    resp = custom_make_response("data", "Signed in successfully", 200)
    resp.set_cookie(
        "auth_token",
        token.decode('utf-8'),
        httponly=True,
        secure=True,
        expires=datetime.datetime.now() + datetime.timedelta(minutes=480)
    )
    return resp


@rms.route('/auth/signout')
@token_required
def signout_all_users(user):
    """sign out users """
    session.pop('username', None)
    resp = custom_make_response("data", "Signed out successfully.", 200)
    resp.set_cookie(
        "auth_token",
        "session over",
        httponly=True,
        secure=True,
        expires="Thu, 01 Jan 1970 00:00:00 GMT"
    )
    return resp
