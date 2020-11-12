"""
this file holds all the user
interface loading routes
methods start as load_
endpoints start as /fe/****
fe - conotes frontend
"""
import jwt
import os
from app.api import rms
from app.api.utils import token_required
from flask import render_template, request


KEY = os.getenv('SECRET_KEY')


@rms.route('/Welcome')
def load_welcome_ui():
    """
    this loads the landing/welcome page of
    our application
    """
    return render_template('welcome.html', title="Welcome")


@rms.route('/admin/fe/signup', methods=['GET'])
@token_required
def load_signup_ui(company):
    """
    load the admin sign up page
    """
    _company = company['company']
    admin_token = request.cookies.get('admin_token')
    admin_data = jwt.decode(admin_token, KEY, algorithm="HS256")
    return render_template(
        'admin-signup.html',
        title="Admin Signup",
        company=_company,
        email=admin_data['email'],
        username=admin_data['username']
    )


@rms.route('/fe/signin', methods=['GET'])
def load_signin_ui():
    """
    load the sign in page
    """
    return render_template("signin.html", title="Sign In")


@rms.route('/fe/who', methods=['GET'])
@token_required
def load_profile_ui(user):
    """
    load the logged in profile ui
    """
    return render_template(
        'profile.html',
        title="Profile",
        username=user['username']
    )
