from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime


db = SQLAlchemy()
ma = Marshmallow()


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


class CompanySchema(ma.Schema):
    class meta:
        """
        this will serialize the company model
        """
        fields = ("id", "company", "joined_at")


company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)


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


class UserSchema(ma.Schema):
    class meta:
        """
        this will serialize the user schema
        """
        fields = ("id", "firstname", "email", "companyId", "role")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


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


class ProjectSchema(ma.Schema):
    class meta:
        """
        this will serialize the project model
        """
        fields = ("id", "project_name", "companyId", "date_from", "date_to")


project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)


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


class BudgetSchema(ma.Schema):
    class meta:
        """
        this will serialize the budget model
        """
        fields = ("id", "companyId", "projectId", "amount")


budget_schema = BudgetSchema()
budgets_schema = BudgetSchema(many=True)


class Employees(db.Model):
    """this  creates the employees model"""
    __tablename__ = "Employees"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    companyId = db.Column(db.Integer, db.ForeignKey('Company.id'))
    projectId = db.Column(db.Integer, db.ForeignKey('Project.id'))

    def __init__(self, firstname, lastname, email, companyId, projectId):
        """initilizing employees model table items"""
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.companyId = companyId
        self.projectId = projectId


class EmployeesSchema(ma.Schema):
    class meta:
        """
        serialize the employees model
        """
        fields = (
            "id", "firstname", "lastname", "email", "companyId",
            "projectId"
            )


employee_schema = EmployeesSchema()
employees_schema = EmployeesSchema(many=True)


class Files(db.Model):
    """this creates the files model"""
    __tablename__ = "Files"

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(120), unique=True, nullable=False)
    companyId = db.Column(db.Integer, db.ForeignKey('Company.id'))
    projectId = db.Column(db.Integer, db.ForeignKey('Project.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    date_created = db.Column(db.DateTime)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    date_reviewed = db.Column(db.DateTime)
    authorized_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    date_authorized = db.Column(db.DateTime)
    status = db.Column(db.String(25), nullable=False)
    url = db.Column(db.String(250), nullable=False)

    def __init__(
        self,
        file_name,
        companyId,
        projectId,
        created_by,
        date_created,
        date_reviewed,
        authorized_by,
        reviewed_by,
        date_authorized,
        status,
        url
    ):
        """intilizing files model items"""
        self.file_name = file_name
        self.companyId = companyId
        self.projectId = projectId
        self.created_by = created_by
        self.date_created = date_created
        self.reviewed_by = reviewed_by
        self.date_reviewed = date_reviewed
        self.authorized_by = authorized_by
        self.date_authorized = date_authorized
        self.status = status
        self.url = url


class FilesSchema(ma.Schema):
    class meta:
        """
        serialize the files model
        """
        fields = (
            "id",
            "file_name",
            "companyId",
            "projectId",
            "created_by",
            "date_created",
            "reviewed_by",
            "date_reviewed",
            "authorized_by",
            "date_authorized",
            "status",
            "url"
        )


files_schema = FilesSchema(many=True)
file_schema = FilesSchema()
