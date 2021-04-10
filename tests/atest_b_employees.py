# this module will hold all tests employees views and
# model in some cases where I want some tests before
# others then you will see the tests enumerated with 
# alphabets.
import jwt
import os
import datetime
import json
from .rmsBaseTest import RmsBaseTest

KEY = os.environ.get('SECRET_KEY')


class TestEmployees(RmsBaseTest):
    # initilize various dictionaries to 
    # mock test data

    _real_admin = {
        "company": "company a",
        "firstname": "kabaki",
        "lastname":"kiarie",
        "mobile":"254712345678",
        "email": "kabaki.kiarie@gmail.com",
        "password": "Banuit*123",
        "role": "Admin",
        "isActive": "true"
    }
    _real_admin_b ={
        "company": "company b",
        "firstname": "wapi",
        "lastname":"niwapi",
        "mobile":"254712345685",
        "email": "wapi.niwapi@gmail.com",
        "password": "Banuit*123",
        "role": "Admin",
        "isActive": "true"
    }
    _admin_with_duplicate_mobile = {
        "company": "company b",
        "firstname": "kabaki",
        "lastname":"kiarie",
        "mobile":"254712345678",
        "email": "wapi.niwapi@gmail.com",
        "password": "Banuit*123",
        "role": "Admin",
        "isActive": "true"
    }
    _admin_with_duplicate_email = {
        "company": "company b",
        "firstname": "kabaki",
        "lastname":"kiarie",
        "mobile":"254712345679",
        "email": "kabaki.kiarie@gmail.com",
        "password": "Banuit*123",
        "role": "Admin",
        "isActive": "true"
    }
    _user_with_correct_login_info = {
        "email": "kabaki.kiarie@gmail.com",
        "password": "Banuit*123"
    }

    def create_admin_employee(self, data={}):
        """
        this is a helper method to keep
        creating the user for the test
        methods that need to post then
        run a test.
        """
        if not data:
            data = self._real_admin
        response = self.client.post(
            '/auth/admin/employees',
            data=json.dumps(self._real_admin),
            content_type='application/json'
        )
        return response
    

    def test_admin_creation(self):
        """test real admin employee creation"""
        response = self.create_admin_employee()
        self.assertEqual(response.status_code, 201)
    
    def test_c_real_admin_login(self):
        """test admin login with real info"""
        response = self.client.post('/auth/signin',
            data=json.dumps(self._user_with_correct_login_info),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_b_getting_single_employee_with_email(self):
        """ test getting a single employee with email address"""
        self.client.post(
            '/auth/admin/employees',
            data=json.dumps(self._real_admin),
            content_type='application/json'
        )
        response = self.client.get('/test/employees/kabaki.kiarie@gmail.com')
        self.assertEqual(response.status_code,200)

    def test_e_admin_with_duplicate_mobile(self):
        """test admin with duplicate mobile"""
        response = self.client.post(
            '/auth/admin/employees',
            data=json.dumps(self._admin_with_duplicate_mobile),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)

    
    def test_f_admin_with_duplicate_email(self):
        """test admin with duplicate email"""
        response = self.client.post(
            '/auth/admin/employees',
            data=json.dumps(self._admin_with_duplicate_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)



    

