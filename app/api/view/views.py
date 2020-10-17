import os
import jwt
import datetime
from flask import request, abort, render_template, jsonify
from app.api import rms
from app.api.model.models import db, User, Employees, Company,\
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
    if Company.query.filter_by(company=data['company']).first():
        abort(
            custom_make_response(
                "error", "please check email for further instructions.", 409
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
    new_company = Company(company, joined_at=datetime.datetime.utcnow())
    db.session.add(new_company)
    db.session.commit()
    return custom_make_response(
        "data", [{
            "Company": company,
            "email": email,
            "message": "Please check your email to complete registration."
        }], 200
    )
