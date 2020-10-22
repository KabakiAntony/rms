"""
this file holds all the user
interface loading routes
methods start as load_
endpoints start as /fe/****
fe - conotes frontend
"""
from app.api import rms
from app.api.utils import company_token_required
from flask import render_template, flash, redirect, url_for
from flask_login import logout_user


@rms.route('/Welcome')
def load_welcome_ui():
    """
    this loads the landing/welcome page of
    our application
    """
    return render_template('welcome.html', title="Welcome")


@rms.route('/admin/fe/signup', methods=['GET'])
@company_token_required
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


@rms.route('/fe/signout', methods=['GET'])
def signout_all_users():
    """
    sign out the current user and
    redirect them to the sign in
    page
    """
    logout_user()
    flash('Signed out successfully.')
    return redirect(url_for('rms.load_signin_ui'))
