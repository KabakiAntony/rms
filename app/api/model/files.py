from app.api.model.models import db, ma


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
    class Meta:
        files = (
            "id",
            "file_name",
            "companyId",
            "projectid",
            "created_by",
            "date_created",
            "reviewed_by",
            "date_reviewed",
            "authorized_by",
            "date_authorized",
            "status",
            "url"
        )


file_schema = FilesSchema()
files_schema = FilesSchema(many=True)
