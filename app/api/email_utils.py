# these are utilities for email sending
import os
import re
from flask import abort
from app.api.utils import custom_make_response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_mail(user_email, the_subject, the_content):
    """send email on relevant user action"""
    message = Mail(
        from_email=("kabaki.antony@gmail.com", "BT Technologies Team"),
        to_emails=user_email,
        subject=the_subject,
        html_content=the_content,
    )
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_KEY"))
        sg.send(message)
    except Exception as e:
        custom_make_response(
            "error",
            f"an error occured sending email contact administrator\
                     {e}",
            500,
        )


def button_style():
    """this returns the style for the button"""
    style = """font-weight:bold;
    background-color: #0096D6;
    border-radius:1.5rem;
    text-decoration: none;
    padding: 7px 28px;
    color:rgb(255, 255, 255);
    margin-top:10px;
    margin-bottom: 10px;
    font-size: 120%;"""
    return style


def password_reset_success_content():
    """return the message for password reset email"""
    content = """
    Hey,
    <br/>
    <br/>
    Your password has been reset successfully, if that was you then you
    don't have to do anything.<br/>
    If you did not carry out this action please click on the link below to
    initiate account recovery.
    <br/>
    <br/>"""
    return content


def password_reset_request_content():
    """return the message for reset reuest email"""
    content = """
    <br/>
    <br/>
    You have received this email, because you requested<br/>
    a password reset link, Click on the reset button below to proceed,<br/>
    If you did not please ignore this email.<br/>
    Note this link will only be active for thirty minutes.
    <br/>
    <br/>
    """
    return content


def non_admin_user_registration_content():
    """return this message when an admin
    creates an account for a user"""
    content = """
    <br/>
    <br/>
    Welcome, an account has been created for you by the,
    company admin, all you need to do is click of the activate
    account button below, you will be prompted to set a password
    for your account and once that is done you can start using
    the account. <br/>
    Note this link will only be active for thirty minutes.
    <br/>
    <br/>
    """
    return content


def email_signature():
    """return email signature"""
    signature = """
    <br/>
    <br/>
    Regards Antony,<br/>
    RMS Admin.
    """
    return signature


def isValidEmail(email):
    """
    checks an email for validity.
    """
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        abort(
            custom_make_response(
                "error", "the email address provided is not valid!", 400
            )
        )
    return True
