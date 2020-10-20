import os
import jwt
import datetime
from app.api import rms
from app.api.model.models import db
from app.api.model.company import Company, company_schema,\
    companies_schema
from flask import request, abort
from app.api.utils import check_for_whitespace, isValidEmail,\
     send_mail, custom_make_response


# getting environment variables
KEY = os.getenv('SECRET_KEY')
signup_url = os.getenv('SIGNUP_URL')


@rms.route('/intent', methods=['POST'])
def company_signup_intent():
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
                "error",
                "One or more mandatory fields has not been filled!", 400)
        )
    # check data for sanity
    check_for_whitespace(data, ['firstname', 'email', 'company'])
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
            "company": company,
            'exp': datetime.datetime.now() +
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
    new_company = Company(company=company, joined_at=datetime.datetime.now())
    db.session.add(new_company)
    db.session.commit()
    return custom_make_response(
        "data",
        company_schema.dump(new_company),
        200
    )


@rms.route('/company', methods=['GET'])
def get_companies():
    """
    get all companies that are registered
    at any onetime
    """
    all_companies = Company.query.all()
    return custom_make_response(
        "data",
        companies_schema.dump(all_companies),
        200
        )
