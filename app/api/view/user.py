import os
import jwt
import datetime
from app.api import rms
from app.api.model import db
from flask import request, abort, session
from app.api.model.user import user_schema, User
# from app.api.model.employees import Employees
from app.api.model.company import Company, company_schema
from app.api.email_utils import send_mail, isValidEmail, \
     button_style, password_reset_success_content,\
     email_signature, non_admin_user_registration_content,\
     password_reset_request_content
from app.api.utils import check_for_whitespace,\
     custom_make_response, token_required,\
     isValidPassword, generate_db_ids,\
     generate_random_password
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
            password = generate_random_password()
        email = user_data['email']
        isActive = user_data['isActive']
        id = generate_db_ids()
        username = user_data['username'] + '.' + id
    except Exception as e:
        # exceptions go to site administrator and email
        # the user gets a friendly error notification
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
    # check if user is on company masterfile
    # if not(
    #     Employees.query.filter_by(email=user_data['email']).first()
    #     and
    #     role != "Admin"
    # ):
    #     abort(
    #         custom_make_response(
    #             "error",
    #             """
    #             The user you are creating an account for
    #             is not on your company masterfile,
    #             Please add them and try again.
    #             """, 400
    #         )
    #     )
    # check if user is already registered
    if User.query.filter_by(email=user_data['email']).first():
        abort(
            custom_make_response(
                "error",
                "A user account with that email already exists,\
                    please use another one and try again.", 409
            )
        )
    isValidPassword(password)
    new_user = User(
        id=id,
        username=username,
        email=email,
        password=password,
        companyId=companyId,
        role=role,
        isActive=isActive
    )
    db.session.add(new_user)
    db.session.commit()
    if role != "Admin":
        token = jwt.encode(
            {
                "id": id,
                "exp": datetime.datetime.utcnow() +
                datetime.timedelta(minutes=30)
            },
            KEY,
            algorithm='HS256'
        )
        subject = """Activate your account."""
        content = f"""
        Hey {username.split('.', 1)[0]},
        {non_admin_user_registration_content()}
        <a href="{password_reset_url}?u={token.decode('utf-8')}"
        style="{button_style()}">Activate account</a>
        {email_signature()}
        """
        send_mail(email, subject, content)
    return custom_make_response(
        "data",
        f"User registered successfully, email sent to {email}\
            for further instructions.",
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
        # exceptions go to site administrator and email
        # the user gets a friendly error notification
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
                """
                User account not found, please register a company
                or have your company admin create an account for you.
                """,
                404
            )
        )
    _user = user_schema.dump(user)
    _password_hash = _user['password']
    if not User.compare_password(_password_hash, password):
        abort(
            custom_make_response(
                "error",
                "Incorrect email and or password, check & try again !",
                401
            )
        )
    _curr_user = user_schema.dump(user)
    if _curr_user['isActive'] != 'true':
        abort(
            custom_make_response(
                "error",
                "Your account is not in active status, contact company admin.",
                401
            )
        )
    token = jwt.encode(
        {
            "id": _curr_user['id'],
            "role": _curr_user['role'],
            'exp': datetime.datetime.utcnow() +
            datetime.timedelta(minutes=480)
        },
        KEY,
        algorithm='HS256'
    )
    session['username'] = _curr_user['username']
    resp = custom_make_response(
        "data",
        "Signed in successfully, preparing your dashboard...",
        200
    )
    resp.set_cookie(
        "auth_token",
        token.decode('utf-8'),
        httponly=True,
        secure=True,
        expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=480)
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
        # exceptions go to site administrator and email
        # the user gets a friendly error notification
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
                "data",
                "An email has been sent to the address on record,\
                    If you don't receive one shortly, please contact\
                        the site admin.",
                200
            )
        )
    this_user = user_schema.dump(user)
    token = jwt.encode(
        {
            "id": this_user['id'],
            'exp': datetime.datetime.utcnow() +
            datetime.timedelta(minutes=30)
        },
        KEY,
        algorithm='HS256'
    )
    subject = """Password reset request"""
    content = f"""
    Hey {this_user['username'].split('.', 1)[0]},
    {password_reset_request_content()}
    <a href="{password_reset_url}?u={token.decode('utf-8')}"
    style="{button_style()}"
    >Reset Password</a>
    {email_signature()}
    """
    send_mail(email, subject, content)
    resp = custom_make_response(
        "data",
        "An email has been sent to the address on record,\
            If you don't receive one shortly, please contact\
                the site admin.",
        202
    )
    return resp


@rms.route('/auth/newpass', methods=['PUT'])
def set_new_password():
    """updates a user password from the reset page"""
    try:
        data = request.get_json()
        email = data['email']
        new_password = data['password']
    except KeyError :
        # add ketError as e to get the exact error
        # exceptions go to site administrator and email
        # the user gets a friendly error notification
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


@rms.route('/auth/suspend', methods=['POST'])
@token_required
def suspend_system_user(user):
    """
    suspend a system user
    """
    try:
        data = request.get_json()
        email = data['email']
    except KeyError:
        # add ketError as e to get the exact error
        # exceptions go to site administrator and email
        # the user gets a friendly error notification
        abort(
            custom_make_response(
                "error",
                "The email field has not been filled, fill and try again.",
                400
            )
        )
    check_for_whitespace(data, ['email'])
    isValidEmail(email)
    User.query.filter_by(email=email).\
        update(dict(isActive='false'))
    db.session.commit()
    return custom_make_response(
        "data",
        "User account suspended successfully",
        200
    )


@rms.route('/auth/reactivate',  methods=['POST'])
@token_required
def reactivate_system_user(user):
    """
    reactivate a suspended user account
    check if account is suspended if not
    then notify the user no need proceeding
    if account if already active.
    """
    try:
        data = request.get_json()
        email = data['email']
    except KeyError:
        # add ketError as e to get the exact error
        # exceptions go to site administrator and email
        # the user gets a friendly error notification
        abort(
            custom_make_response(
                "error",
                "The email field has not been filled, fill and try again.",
                400
            )
        )
    check_for_whitespace(data, ['email'])
    isValidEmail(email)
    User.query.filter_by(email=email).\
        update(dict(isActive='true'))
    db.session.commit()
    return custom_make_response(
        "data",
        "User account activated successfully",
        200
    )
