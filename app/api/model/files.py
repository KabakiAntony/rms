from app.api.model import db, ma


class Files(db.Model):
    """this creates the files model"""
    __tablename__ = "Files"

    id = db.Column(db.String(20), primary_key=True)
    fileName = db.Column(db.String(120), unique=True, nullable=False)
    companyId = db.Column(db.String(20), db.ForeignKey('Company.id'))
    projectId = db.Column(db.String(20), db.ForeignKey('Project.id'))
    createdBy = db.Column(db.String(20), db.ForeignKey('Users.id'))
    dateCreated = db.Column(db.DateTime)
    reviewedBy = db.Column(db.String(20), db.ForeignKey('Users.id'))
    dateReviewed = db.Column(db.DateTime)
    authorizedBy = db.Column(db.String(20), db.ForeignKey('Users.id'))
    dateAuthorized = db.Column(db.DateTime)
    fileStatus = db.Column(db.String(25), nullable=False)
    fileUrl = db.Column(db.String(250), nullable=False)

    def __init__(
        self,
        fileName,
        companyId,
        projectId,
        createdBy,
        dateCreated,
        dateReviewed,
        authorizedBy,
        reviewedBy,
        dateAuthorized,
        fileStatus,
        fileUrl
    ):
        """intilizing files model items"""
        self.fileName = fileName
        self.companyId = companyId
        self.projectId = projectId
        self.createdBy = createdBy
        self.dateCreated = dateCreated
        self.reviewedBy = reviewedBy
        self.dateReviewed = dateReviewed
        self.authorizedBy = authorizedBy
        self.dateAuthorized = dateAuthorized
        self.fileStatus = fileStatus
        self.fileUrl = fileUrl


class FilesSchema(ma.Schema):
    class Meta:
        files = (
            "id",
            "fileName",
            "companyId",
            "projectid",
            "createdBy",
            "dateCreated",
            "reviewedBy",
            "dateReviewed",
            "authorizedBy",
            "dateAuthorized",
            "fileStatus",
            "fileUrl"
        )


file_schema = FilesSchema()
files_schema = FilesSchema(many=True)
