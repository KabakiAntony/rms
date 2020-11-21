from app.api.model.models import db, ma


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
    class Meta:
        fields = (
            "id",
            "firstname",
            "lastname",
            "email",
            "companyId",
            "projectId"
        )


employee_schema = EmployeesSchema()
employees_schema = EmployeesSchema(many=True)
