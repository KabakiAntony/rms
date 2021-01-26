from app.api.model import db, ma


class Project(db.Model):
    """
    this creates the project model
    """
    __tablename__ = "Project"

    id = db.Column(db.String(20), primary_key=True)
    project_name = db.Column(db.String(100), nullable=False, unique=True)
    companyId = db.Column(db.String(20), db.ForeignKey('Company.id'))
    date_from = db.Column(db.Date)
    date_to = db.Column(db.Date)

    def __init__(self, id, project_name, companyId, date_from, date_to):
        """initializing inputs for this model"""
        self.id = id
        self.project_name = project_name
        self.companyId = companyId
        self.date_from = date_from
        self.date_to = date_to


# user['username'].split('.', 1)[0]
class ProjectSchema(ma.Schema):
    class Meta:
        fields = ("id", "project_name", "companyId", "date_from", "date_to")


project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
