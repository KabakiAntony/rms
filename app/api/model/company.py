"""
this will handle the company
model for the db
"""
from app.api.model import db, ma
from datetime import datetime


class Company(db.Model):
    """
    this creates the company model
    """
    __tablename__ = "Company"

    id = db.Column(db.String(20), primary_key=True)
    company = db.Column(db.String(64), index=True, unique=True)
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, id, company, joined_at):
        """
        initializing company db values
        """
        self.id = id
        self.company = company
        self.joined_at = joined_at


class CompanySchema(ma.Schema):
    class Meta:
        fields = ("id", "company", "joined_at")


company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)
