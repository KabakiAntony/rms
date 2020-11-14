"""
it will hold the reusable
functions.
"""
import re
import os
import jwt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from functools import wraps
from flask import jsonify, make_response, abort, request
from app.api.model.company import Company, company_schema
from app.api.model.user import User, user_schema


KEY = os.getenv('SECRET_KEY')


def custom_make_response(key, message, status):
    """
    this is a custom make response for readability
    to avoid repeating the parts that make up a return
    message.
    """
    raw_dict = {"status": status}
    raw_dict[key] = message
    return make_response(jsonify(raw_dict), status)


def check_model_return(returned):
    """
    checks whether there was a return from the models
    assigns a 404/200 accordingly or 201 in the case of creation
    and assigns it a better message for the user
    """
    if not returned:
        message = "the resource you are looking for was not found!"
        status = 404
        response = custom_make_response("error", message, status)
    else:
        message = returned
        status = 200
        response = custom_make_response("data", message, status)
    return response


def isValidEmail(email):
    """
    checks an email for validity.
    """
    if not re.match(
        r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
        email
    ):
        abort(custom_make_response(
            "error", "the email address provided is not valid!", 400))
    return True


def isValidPassword(password):
    """
    check if the supplied password meets the
    expectations.
    """
    if len(password) < 6 or len(password) > 20:
        abort(
            custom_make_response(
                "error",
                "Password should be atleast 6 characters & not more than 20",
                400)
        )

    lowercase_reg = re.search("[a-z]", password)
    uppercase_reg = re.search("[A-Z]", password)
    number_reg = re.search("[0-9]", password)

    if not lowercase_reg or not uppercase_reg or not number_reg:
        abort(custom_make_response(
            "error",
            "Password should contain at least 1 number,\
                 1 small letter & 1 Capital letter",
            400)
        )


def check_for_whitespace(data, items_to_check):
    """
    check if the data supplied has whitespace
    """
    for key, value in data.items():
        if key in items_to_check and not value.strip():
            abort(
                custom_make_response(
                    "error",
                    f"{key} cannot be left blank!",
                    400
                )

            )
    return True


def send_mail(user_email, the_subject, the_content):
    """ send email on relevant user action """
    message = Mail(
        from_email=('kabaki.antony@gmail.com', 'RMS Team'),
        to_emails=user_email,
        subject=the_subject,
        html_content=the_content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_KEY'))
        sg.send(message)
    except Exception as e:
        custom_make_response(
                "error", f"an error occured sending email contact administrator\
                     {e}", 500)


def token_required(f):
    """
    this token is used to allow the user to access
    certain routes
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        user_token = None
        company_token = None
        if (request.cookies.get('auth_token') or
            request.args.get('in') or
                request.args.get('u')):
            user_token = (
                request.cookies.get('auth_token') or
                request.args.get('u')
            )
            company_token = request.args.get('in')
        if not (user_token or company_token):
            return custom_make_response("error", "Token is missing", 401)
        try:
            if user_token:
                data = jwt.decode(user_token, KEY, algorithm="HS256")
                current_user = User.query\
                    .filter_by(username=data['username']).first()
                _data = user_schema.dump(current_user)
            if company_token:
                data = jwt.decode(company_token, KEY, algorithms="HS256")
                current_company = Company.query\
                    .filter_by(company=data['company']).first()
                _data = company_schema.dump(current_company)
        except Exception as e:
            return custom_make_response("error", f"Token {e}", 401)
        return f(_data, *args, **kwargs)
    return decorated
