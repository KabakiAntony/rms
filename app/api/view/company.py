import os
import jwt
import datetime
from app.api import rms
from app.api.model import db
from app.api.model.company import Company, companies_schema
from flask import request, abort
from app.api.email_utils import isValidEmail, send_mail, button_style
from app.api.utils import (
    check_for_whitespace,
    custom_make_response,
    token_required,
    generate_db_ids,
)


# getting environment variables
KEY = os.environ.get("SECRET_KEY")
signup_url = os.getenv("SIGNUP_URL")


@rms.route("/intent", methods=["POST"])
def company_signup_intent():
    """
    send a sign up link on the email to
    would be customers
    """
    try:
        data = request.get_json()
        # username = data["username"]
        email = data["email"]
        company = data["company"]
        id = generate_db_ids()
    except Exception:
        abort(
            custom_make_response(
                "error",
                "One or more mandatory fields has not been filled!", 400
            )
        )
    # check data for sanity
    check_for_whitespace(data, ["email", "company"])
    isValidEmail(email)
    # check if the company is already registered
    # the feedback message when a company is already
    # registered needs refining
    if Company.query.filter_by(company=data["company"]).first():
        abort(
            custom_make_response(
                "error",
                "Company exists,\
                     contact your company administrator",
                409,
            )
        )
    token = jwt.encode(
        {
            "email": email,
            # "username": username,
            "company": company,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        },
        KEY,
        algorithm="HS256",
    )
    # send signup intent email
    subject = f"""Thank you for requesting to register {company}."""
    content = f"""
    Welcome ,
    <br/>
    <br/>
    We are grateful to have you.<br/>
    Please click on sign up below to register your personal
    information to start using the system.<br/>Kindly note this
    link will only be active for thirty minutes.
    <br/>
    <br/>
    <a href="{signup_url}?in={token.decode('utf-8')}"
    style="{button_style()}">Sign Up</a>
    <br/>
    <br/>
    Regards Antony,<br/>
    RMS Admin.
    """
    new_company = Company(
        id=id, company=company, joined_at=datetime.datetime.utcnow())
    db.session.add(new_company)
    db.session.commit()
    send_mail(email, subject, content)
    resp = custom_make_response(
        "data",
        f"Request to register {company} successful,\
             see {email} for more information.",
        201,
    )
    resp.set_cookie(
        "admin_token",
        token.decode("utf-8"),
        httponly=True,
        secure=True,
        expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=180),
    )
    return resp


@rms.route("/companies", methods=["GET"])
@token_required
def get_companies(user):
    """
    get all companies that are registered
    at any onetime
    """
    # please note only the site admin
    # should have access to this data
    all_companies = Company.query.all()
    return custom_make_response(
        "data", companies_schema.dump(all_companies), 200)
