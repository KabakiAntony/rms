"""
it will hold the reusable
functions.
"""
import re
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import jsonify, make_response, abort


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
        message = "no data was found!"
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
        print(e)
