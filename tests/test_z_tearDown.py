# this is not a test
# it just runs tearDown
from .rmsBaseTest import RmsBaseTest
from app.api.model.models import db


class TestTearDown(RmsBaseTest):
    def test_tearing_down(self):
        print("tearing down the database")
        db.session.remove()
        db.drop_all()
