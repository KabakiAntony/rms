"""
this will create the user model(table)
and its serialization.
"""
from app.api.model import db, ma
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    this creates the system users model
    """

    __tablename__ = "Users"

    id = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    companyId = db.Column(db.String(20), db.ForeignKey("Company.id"))
    role = db.Column(db.String(25), nullable=False)
    isActive = db.Column(db.String(25), default="False", nullable=False)

    def __init__(self, id, username, email, password, role, companyId, isActive):
        """initilize user db values"""
        self.id = id
        self.username = username
        self.email = email
        self.password = self.hash_password(password)
        self.companyId = companyId
        self.role = role
        self.isActive = isActive

    def hash_password(self, password):
        """create a password hash for storage"""
        password_hash = generate_password_hash(str(password))
        return password_hash

    def compare_password(hashed_password, password):
        """compare a plain password with its stored hash"""
        return check_password_hash(hashed_password, str(password))


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "username",
            "password",
            "email",
            "companyId",
            "role",
            "isActive",
        )


user_schema = UserSchema()
users_schema = UserSchema(many=True)
