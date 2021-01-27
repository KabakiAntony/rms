from app.api.model import db, ma


class Employees(db.Model):
    """this  creates the employees model"""
    __tablename__ = "Employees"

    id = db.Column(db.String(20), primary_key=True)
    companyId = db.Column(db.String(20), db.ForeignKey('Company.id'))
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    mobile = db.Column(db.Integer(), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def __init__(self, id, companyId, firstname, lastname, mobile, email):
        """initilizing employees model table items"""
        self.id = id
        self.companyId = companyId
        self.firstname = firstname
        self.lastname = lastname
        self.mobile = mobile
        self.email = email


class EmployeesSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "companyId",
            "firstname",
            "lastname",
            "mobile",
            "email"
            
        )


employee_schema = EmployeesSchema()
employees_schema = EmployeesSchema(many=True)
