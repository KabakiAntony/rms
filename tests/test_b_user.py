# this will hold tests for user model
# and all related routines
import json
from .rmsBaseTest import RmsBaseTest


class TestUser(RmsBaseTest):
    # intialize various dictionaries for use in testing
    _real_user = {
        "company": "company a",
        "username": "kabaki",
        "email": "kabaki.kiarie@gmail.com",
        "password": "Banuit*123"
    }
    _user_with_invalid_email = {
        "username": "kabaki",
        "email": "kabaki.kiarie@gmail",
        "password": "Banuit*123",
        "company": "company a"
    }
    _user_with_lower_case_password = {
        "username": "kabaki",
        "email": "kabaki.kiarie@gmail.com",
        "password": "banuit*123",
        "company": "company a"
    }
    _user_with_upper_case_password = {
        "username": "kabaki",
        "email": "kabaki.kiarie@gmail.com",
        "password": "BANUIT*123",
        "company": "company a"
    }
    _user_with_no_special_characters_password = {
        "username": "kabaki",
        "email": "kabaki.kiarie@gmail.com",
        "password": "Banuit123",
        "company": "company a"
    }
    _user_with_missing_fields = {
        "username": "kabaki",
        "email": "",
        "password": "Banuit*123",
        "company": "company a"
    }
    _user_with_short_password = {
        "username": "kabaki",
        "email": "kabaki.kiarie@gmail.com",
        "password": "B*12",
        "company": "company a"
    }
    _user_with_long_password = {
        "username": "kabaki",
        "email": "kabaki.kiarie@gmail.com",
        "password": "Banuit*123fsgsssgfr123wt34t4rg4t3$SWA$$%w^W$23tg3",
        "company": "company a"
    }
    _user_login_with_correct_information = {
        "email": "kabaki.kiarie@gmail.com",
        "password": "Banuit*123"
    }
    _user_login_with_incorrect_password = {
        "email": "kabaki.kiarie@gmail.com",
        "password": "Banuit*123s"
    }
    _unregistered_user = {
        "email": "kabaki@gmail.com",
        "password": "Banuit*123"
    }

    def user_creation_post(self, data={}):
        """
        this is a helper method to keep
        creating the user for the test
        methods that need to post then
        run a test.
        """
        if not data:
            data = self._real_user
        response = self.client.post(
            '/admin/signup',
            data=json.dumps(self._real_user),
            content_type='application/json'
        )
        return response

    def test_real_admin_signup(self):
        """test real admin signup"""
        response = self.user_creation_post()
        self.assertEqual(response.status_code, 201)

    def test_signup_already_existing_admin(self):
        """Test signing up an already admin"""
        self.user_creation_post()
        response = self.user_creation_post()
        self.assertEqual(response.status_code, 409)

    def test_signup_with_invalid_email(self):
        """test signing up with an invalid email"""
        response = self.client.post(
            '/admin/signup',
            data=json.dumps(self._user_with_invalid_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_signup_user_with_missing_fields(self):
        """test signing up user with some fields missing"""
        response = self.client.post(
            '/admin/signup',
            data=json.dumps(self._user_with_missing_fields),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_signup_an_already_existing_user(self):
        """test signing up and already existing user"""
        self.user_creation_post()
        response = self.user_creation_post()
        self.assertEqual(response.status_code, 409)

    def test_signup_user_with_long_password(self):
        """test signing up a user with a long password"""
        response = self.client.post(
            '/admin/signup',
            data=json.dumps(self._user_with_long_password),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)

    def test_signup_user_with_short_password(self):
        """test signing up a user with a short password"""
        response = self.client.post(
            '/admin/signup',
            data=json.dumps(self._user_with_short_password),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)

    def test_signup_user_with_lower_case_password(self):
        """test signing up a user with all lower case password"""
        response = self.client.post(
            '/admin/signup',
            data=json.dumps(self._user_with_lower_case_password),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)

    def test_signup_user_with_upper_case_password(self):
        """test signing up a user with upper case password"""
        response = self.client.post(
            '/admin/signup',
            data=json.dumps(self._user_with_upper_case_password),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)

    def test_signup_user_with_no_special_characters_password(self):
        """test signing up a user with password with no special chars"""
        response = self.client.post(
            '/admin/signup',
            data=json.dumps(
                self._user_with_no_special_characters_password
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)
