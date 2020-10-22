"""
this will create the user model(table)
and its serialization.
"""
from flask_login import UserMixin, LoginManager
from app.api.model.models import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()


class User(UserMixin, db.Model):
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

    def __init__(self, firstname, email, password, role, companyId, isActive):
        """initilize user db values"""
        self.firstname = firstname
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
            "firstname",
            "password",
            "email",
            "companyId",
            "role",
            "isActive"
        )


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@login_manager.user_loader
def load_user(id):
    """
    load the user id for
    session creation in flask-login
    """
    return User.query.get(int(id))
