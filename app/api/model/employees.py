from app.api.model import db, ma


class Employees(db.Model):
    """this  creates the employees model"""
    __tablename__ = "Employees"

    id = db.Column(db.String(20), primary_key=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.Integer(), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    companyId = db.Column(db.String(20), db.ForeignKey('Company.id'))

    def __init__(self, id, firstname, lastname, mobile, email, companyId):
        """initilizing employees model table items"""
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.mobile = mobile
        self.email = email
        self.companyId = companyId


class EmployeesSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "firstname",
            "lastname",
            "mobile",
            "email",
            "companyId",
        )


employee_schema = EmployeesSchema()
employees_schema = EmployeesSchema(many=True)
