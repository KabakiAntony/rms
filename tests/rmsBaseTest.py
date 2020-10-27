# this class will hold my setUp and tearDown
# methods for all my test modules
import unittest
from app import create_app
from app.api.model.models import db


class RmsBaseTest(unittest.TestCase):
    """create setUp and tearDown for RMS"""
    def setUp(self):
        """set up tests all modules"""
        self.app = create_app()
        self.app.config.from_object('config.TestingConfig')
        self.client = self.app.test_client()
        db.create_all()
