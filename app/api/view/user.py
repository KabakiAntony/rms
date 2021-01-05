import os
import jwt
import datetime
from app.api import rms
from app.api.model import db
from flask import request, abort, session
from app.api.model.user import user_schema, User
from app.api.model.company import Company, company_schema
from app.api.utils import check_for_whitespace, isValidEmail,\
     send_mail, custom_make_response, token_required,\
     isValidPassword, button_style, password_reset_request_content,\
     password_reset_success_content, email_signature
from werkzeug.security import generate_password_hash


# get environment variables
KEY = os.getenv('SECRET_KEY')
signup_url = os.getenv('SIGNUP_URL')
password_reset_url = os.getenv('PASSWORD_RESET_URL')


@rms.route('/auth/signup', methods=['POST'])
def signup_system_users():
    """
    signup system users
    """
    try:
        user_data = request.get_json()
        role = user_data['role']
        if role == "Admin":
            this_company = Company.query\
                .filter_by(company=user_data['company']).first()
            _company = company_schema.dump(this_company)
            companyId = _company['id']
            password = user_data['password']
        else:
            companyId = user_data['companyId']
            # while this password is not used anywhere
            # I have to find a better way to generate randomn
            # passwords those that will be used for data sanity
            # but the user is prompted to create a new password 
            # on the first time they are logging in
            password = "Banuit@123"
        username = user_data['username']
        email = user_data['email']
        isActive = user_data['isActive']
    except Exception as e:
        abort(
            custom_make_response(
                "error",
                f"{e} field has not been filled!", 400)
        )
    # check data for sanity incase it bypass js on the frontend
    check_for_whitespace(
        user_data,
        ['companyId', 'username', 'email', 'password', 'role', 'status']
    )
    isValidEmail(email)
    # check if user is already registered
    if User.query.filter_by(email=user_data['email']).first():
        abort(
            custom_make_response(
                "error",
                "User exists, please use another email!", 409
            )
        )
    # check if username is already used
    if User.query.filter_by(username=user_data['username']).first():
        abort(
            custom_make_response(
                "error",
                "User exists, please use another username!", 409
            )
        )
    isValidPassword(password)
    new_user = User(
        username=username,
        email=email,
        password=password,
        companyId=companyId,
        role=role,
        isActive=isActive
    )
    db.session.add(new_user)
    db.session.commit()
    return custom_make_response(
        "data",
        f"{ username } registered successfully.",
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
    _curr_user = user_schema.dump(user)
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
    session['username'] = _curr_user['username']
    resp = custom_make_response(
        "data",
        "Sign In successful, preparing your dashboard...",
        200
    )
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


@rms.route('/auth/forgot', methods=['POST'])
def forgot_password():
    """ send reset password email """
    try:
        user_data = request.get_json()
        email = user_data['email']
    except Exception as e:
        abort(
            custom_make_response(
                "error",
                f"{e} You have not entered an email!",
                400
            )
        )
    check_for_whitespace(user_data, ['email'])
    isValidEmail(email)
    user = User.query.filter_by(email=user_data['email']).first()
    if not user:
        abort(
            custom_make_response(
                "error",
                "User not found, Please sign up to use the system!",
                404
            )
        )
    this_user = user_schema.dump(user)
    token = jwt.encode(
        {
            "username": this_user['username'],
            'exp': datetime.datetime.now() +
            datetime.timedelta(minutes=30)
        },
        KEY,
        algorithm='HS256'
    )
    subject = """Password reset request"""
    content = f"""
    Hey {this_user['username']},
    {password_reset_request_content()}
    <a href="{password_reset_url}?u={token.decode('utf-8')}"
    style="{button_style()}"
    >Reset Password</a>
    {email_signature()}
    """
    send_mail(email, subject, content)
    resp = custom_make_response(
        "data",
        f"Email sent successfully, head over to {email} for instructions.",
        202
    )
    resp.set_cookie(
        "reset_token",
        token.decode('utf-8'),
        httponly=True,
        secure=True,
        expires=datetime.datetime.now() + datetime.timedelta(minutes=30)
    )
    return resp


@rms.route('/auth/newpass', methods=['PUT'])
def set_new_password():
    """updates a user password from the reset page"""
    pass_reset_token = request.cookies.get('reset_token')
    if not pass_reset_token:
        abort(
            custom_make_response(
                "error",
                "A required piece of authentication seems to be missing!",
                401
            )
        )
    try:
        data = request.get_json()
        email = data['email']
        new_password = data['password']
    except KeyError:
        abort(
            custom_make_response(
                "error",
                "One or more mandatory fields has not been filled!",
                400
            )
        )
    check_for_whitespace(data, ['email', 'password'])
    isValidEmail(email)
    isValidPassword(new_password)
    User.query.filter_by(email=data['email']).\
        update(dict(
            password=f'{generate_password_hash(str(new_password))}'))
    db.session.commit()
    subject = """Password reset success."""
    content = f"""
    {password_reset_success_content()}
    <a href="/forgot"
    style="{button_style()}"
    >Forgot Password</a>
    {email_signature()}
    """
    send_mail(email, subject, content)
    return custom_make_response(
        "data",
        "Your password has been reset successfully",
        200
    )
