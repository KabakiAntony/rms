from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


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

    def __repr__(self):
        """
        format how the company info will be returned from the db
        """
        return '{}{}{}'.format(self.id, self.company, self.joined_at)


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

    def __repr__(self):
        """this formats how a user will be returned from the db"""
        return '<{}:{}:{}>'.format(self.id, self.firstname, self.email)


class Project(db.Model):
    """
    this creates the project model
    """
    __tablename__ = "Project"

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False, unique=True)
    companyId = db.Column(db.Integer, db.ForeignKey('Company.id'))
    date_from = db.Column(db.DateTime)
    date_to = db.Column(db.DateTime)

    def __init__(self, project_name, companyId, date_from, date_to):
        """initializing inputs for this model"""
        self.project_name = project_name
        self.companyId = companyId
        self.date_from = date_from
        self.date_to = date_to

    def __repr__(self):
        """this formats the project object for view"""
        return "{}{}".format(self.project_name, self.companyId)


class Budget(db.Model):
    """
    this creates the  budget model
    """
    __tablename__ = "Budget"

    id = db.Column(db.Integer, primary_key=True)
    companyId = db.Column(db.Integer, db.ForeignKey('Company.id'))
    projectId = db.Column(db.Integer, db.ForeignKey('Project.id'))
    amount = db.Column(db.Integer, nullable=False)

    def __init___(self, companyId, projectId, amount):
        """initializing objects for budget model"""
        self.companyId = companyId
        self.projectId = projectId
        self.amount = amount

    def __repr__(self):
        """format how the budget object will be represented"""
        return "{}{}{}".format(self.companyId, self.projectId, self.amount)


class Employees(db.Model):
    """this  creates the employees model"""
    __tablename__ = "Employees"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    companyId = db.Column(db.Integer, db.ForeignKey('Company.id'))
    project = db.Column(db.Integer, db.ForeignKey('Project.id'))

    def __init__(self, firstname, lastname, email, companyId, projectId):
        """initilizing employees model table items"""
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.companyId = companyId
        self.projectId = projectId

    def __repr__(self):
        """formating the employees object for view"""
        return "{}{}{}{}{}".format(
            self.firstname,
            self.lastname,
            self.email,
            self.companyId,
            self.project
        )
