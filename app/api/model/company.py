"""
this will handle the company
model for the db
"""
from app.api.model.models import db, ma
from datetime import datetime


class Company(db.Model):
    """
    this creates the company model
    """
    __tablename__ = "Company"

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(64), index=True, unique=True)
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, company, joined_at):
        """
        initializing company db values
        """
        self.company = company
        self.joined_at = joined_at

    # def __repr__(self):
    #     return f"'id': {self.id},\
    #         'company': {self.company},\
    #             'joined_at': {self.joined_at}"

    # def serialize_company(iterable):
    #     """
    #     serialize company data from db
    #     """
    #     list_data = []
    #     for list_item in iterable:
    #         list_format = {
    #             "id": list_item[0],
    #             "company": list_item[1],
    #             "joined_at": list_item[2]
    #             }
    #         list_data.append(list_format)
    #     return list_data


class CompanySchema(ma.Schema):
    class Meta:
        fields = ("id", "company", "joined_at")


company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)
