import os
import jwt
import datetime
from app.api import rms
from app.api.model.models import db
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
        "Signed in successfully, redirecting to your dashboard...",
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
    {password_reset_success_content()}
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
    {password_reset_request_content()}
    <a href="/fe/forgot"
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
