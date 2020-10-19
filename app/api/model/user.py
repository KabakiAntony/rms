"""
this will create the user model(table)
and its serialization.
"""
from app.api.model.models import db


class User(db.Model):
    """
    this creates the system users model
    """
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    companyId = db.Column(db.Integer, db.ForeignKey('Company.id'))
    role = db.Column(db.String(25), nullable=False)
    isActive = db.Column(db.String(25), default='False', nullable=False)

    def __init__(self, firstname, email, password, role, companyId):
        """initilize user db values"""
        self.firstname = firstname
        self.email = email
        self.password = password
        self.companyId = companyId
        self.role = role
