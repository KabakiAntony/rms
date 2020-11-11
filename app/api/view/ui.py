"""
this file holds all the user
interface loading routes
methods start as load_
endpoints start as /fe/****
fe - conotes frontend
"""
from app.api import rms
from app.api.utils import token_required
from flask import render_template, redirect, url_for, request
# from app.api.model.user import User, user_schema


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
    return render_template(
        'admin-signup.html',
        title="Sign Up",
        company=_company,
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


# @rms.route('/fe/signout', methods=['GET'])
# def signout_all_users():
#     """
#     sign out the current user and
#     redirect them to the sign in
#     page
#     """
#     logout_user()
#     return redirect(url_for('rms.load_signin_ui'))
