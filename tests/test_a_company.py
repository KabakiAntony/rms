# this will hold tests for company creation
# and all other company involved routines
import json
from .rmsBaseTest import RmsBaseTest


class TestCompany(RmsBaseTest):
    # initiliaze company info for testing
    _real_company = {
        "username": "kabaki",
        "email": "kabaki.kiarie@gmail.com",
        "company": "company a"
    }
    _company_with_missing_fields = {
        "username": "kabaki",
        "email": "",
        "company": "company a"
    }
    _company_with_invalid_email = {
        "username": "kabaki",
        "email": "kabaki.gmail.com",
        "company": "company a"
    }

    def company_creation_post(self, data={}):
        """
        This is just a helper method for the
        test cases that need to post data.
        """
        if not data:
            data = self._real_company
        response = self.client.post(
            '/intent',
            data=json.dumps(self._real_company),
            content_type='application/json'
        )
        return response

    def test_company_creation(self):
        """ test creating a company with real data"""
        response = self.company_creation_post()
        self.assertEqual(response.status_code, 201)

    def test_getting_all_companies(self):
        """test getting all companies"""
        self.company_creation_post()
        response = self.client.get('/company')
        self.assertEqual(response.status_code, 200)

    def test_creating_a_company_with_fields_missing(self):
        """test creating a company with missing fields"""
        response = self.client.post(
            '/intent',
            data=json.dumps(self._company_with_missing_fields),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_recreating_a_company(self):
        """test recreating a company"""
        self.company_creation_post()
        response = self.client.post(
            '/intent',
            data=json.dumps(self._real_company),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)

    def test_creating_a_company_with_invalid_admin_email(self):
        """test creating a company with invalid admin email"""
        response = self.client.post(
            '/intent',
            data=json.dumps(self._company_with_invalid_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
