import os
import jwt
import datetime
from flask import request, abort, render_template, jsonify
from app.api import rms
from app.api.model.models import User, Employees, Company,\
    Files, Budget, Project
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
                "error", "keys should be 'firstname','email','company'", 400)
        )
    # check data for sanity
    check_for_whitespace(data, ['firsname', 'email', 'company'])
    isValidEmail(email)
    # check if the company is already registered
    if User.query.get(company):
        abort(
            custom_make_response(
                "error", "seems like the company is already registered", 409
            )
        )
    token = jwt.encode(
        {
            "email": email,
            'exp': datetime.datetime.utcnow() +
            datetime.timedelta(minutes=1800)
        },
        KEY,
        algorithm='HS256'
    )
    # send signup intent email
    subject = """Thank for your interest in RMS"""
    content = f"""
    Hey {firstname},
    <br/>
    <br/>
    We are grateful for your interest on signing up with us<br/>
    Please logon to the below link to register.
    <a href="{signup_url}?in={token.decode('utf-8')}">link</a>.
    <br/>
    <br/>
    Regards Antony,<br/>
    RMS Admin.
    """
    send_mail(email, subject, content)
    return custom_make_response(
        "data", [{
            "firstname": firstname,
            "email": email
        }], 200
    )
