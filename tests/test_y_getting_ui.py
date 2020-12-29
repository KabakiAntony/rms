import jwt
import os
import datetime
from .rmsBaseTest import RmsBaseTest

KEY = os.environ.get('SECRET_KEY')


class TestGettingUI(RmsBaseTest):
    _real_company = {
        "username": "kabaki",
        "email": "kabaki.kiarie@gmail.com",
        "company": "company a"
    }

    def test_getting_homepage(self):
        """test getting the welcome page"""
        response = self.client.get('/welcome')
        self.assertEqual(response.status_code, 200)

    def test_getting_signin_page(self):
        """test getting the signin page"""
        response = self.client.get('/signin')
        self.assertEqual(response.status_code, 200)

    def test_getting_forgot_password_page(self):
        """test getting forgot password page"""
        response = self.client.get('/forgot')
        self.assertEqual(response.status_code, 200)

    def test_getting_new_password_page_without_a_token(self):
        response = self.client.get('/new-password')
        self.assertEqual(response.status_code, 401)

    def test_getting_admin_signup_without_a_token(self):
        response = self.client.get('/admin/signup')
        self.assertEqual(response.status_code, 401)

    def test_getting_admin_signup_with_a_token(self):
        token = jwt.encode(
            {
                "email": "kabaki.kiarie@gmail.com",
                "username": "kabaki",
                "company": "company a",
                'exp': datetime.datetime.now() +
                datetime.timedelta(minutes=10)
            },
            KEY, algorithm='HS256'
        )
        self.client.set_cookie(
            "admin_token",
            token.decode('utf-8'),
            httponly=False,
            secure=True,
            expires=datetime.datetime.now() + datetime.timedelta(minutes=10)
        )
        response = self.client.get(
            f"/admin/signup?in={token.decode('utf-8')}")
        self.assertEqual(response.status_code, 401)
