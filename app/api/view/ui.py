"""
this file holds all the user
interface loading routes
"""
import jwt
import os
from app.api import rms
from app.api.utils import token_required, custom_make_response
from flask import render_template, request, abort


KEY = os.getenv('SECRET_KEY')


@rms.route('/Welcome')
def load_welcome_ui():
    """
    this loads the landing/welcome page of
    our application
    """
    return render_template('welcome.html', title="Welcome")


@rms.route('/admin/signup', methods=['GET'])
@token_required
def load_signup_ui(company):
    """
    load the admin sign up page
    """
    _company = company['company']
    admin_token = request.cookies.get('admin_token')
    if not admin_token:
        abort(
            custom_make_response(
                "error",
                "A required piece of authentication seems to be missing!",
                401
            )
        )
    admin_data = jwt.decode(admin_token, KEY, algorithm="HS256")
    return render_template(
        'admin-signup.html',
        title="Admin Signup",
        company=_company,
        email=admin_data['email'],
        username=admin_data['username']
    )


@rms.route('/signin')
def _signin_ui():
    """
    load the sign in page
    """
    return render_template("signin.html", title="Sign In")


@rms.route('/dashboard', methods=['GET'])
@token_required
def load_profile_ui(user):
    """
    load the logged in profile ui
    """
    return render_template(
        'dashboard.html',
        title="Dashboard",
        username=user['username'],
        role=user['role']
    )


@rms.route('/forgot')
def _forgot_password_ui():
    """
    forgot password ui
    """
    return render_template('forgot.html', title="Forgot Password")


@rms.route('/new-password', methods=['GET'])
@token_required
def load_password_reset_ui(user):
    """
    load the password reset ui
    """
    return render_template('new-password.html', title="New Password")


@rms.route('/contact')
def _contact_ui():
    """
    contact ui
    """
    return render_template('contact.html', title="Contact us")
