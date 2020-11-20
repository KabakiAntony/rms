from app.api.model.models import db, ma
from datetime import datetime


class Project(db.Model):
    """
    this creates the project model
    """
    __tablename__ = "Project"

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False, unique=True)
    companyId = db.Column(db.Integer, db.ForeignKey('Company.id'))
    date_from = db.Column(db.DateTime, default=datetime.utcnow)
    date_to = db.Column(db.DateTime)

    def __init__(self, project_name, companyId, date_from, date_to):
        """initializing inputs for this model"""
        self.project_name = project_name
        self.companyId = companyId
        self.date_from = date_from
        self.date_to = date_to


class ProjectSchema(ma.Schema):
    class Meta:
        fields = ("id", "project_name", "companyId", "date_from", "date_to")


project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
