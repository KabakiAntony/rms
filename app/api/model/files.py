from app.api.model import db, ma


class Files(db.Model):
    """this creates the files model"""

    __tablename__ = "Files"

    id = db.Column(db.String(20), primary_key=True)
    companyId = db.Column(db.String(20), db.ForeignKey("Company.id"))
    projectId = db.Column(db.String(20), db.ForeignKey("Project.id"))
    fileType = db.Column(db.String(10), nullable=False)
    # fileVersion = db.Column(db.String(2), nullable=False)
    fileAmount = db.Column(db.Float, nullable=False)
    createdBy = db.Column(db.String(20), db.ForeignKey("Users.id"))
    dateCreated = db.Column(db.Date)
    authorizedOrRejectedBy = db.Column(db.String(20), db.ForeignKey("Users.id"))
    dateAuthorizedOrRejected = db.Column(db.Date)
    fileStatus = db.Column(db.String(25), nullable=False)
    fileName = db.Column(db.String(100), nullable=False)

    def __init__(
        self,
        id,
        companyId,
        projectId,
        fileType,
        # fileVersion,
        fileAmount,
        createdBy,
        dateCreated,
        authorizedOrRejectedBy,
        dateAuthorizedOrRejected,
        fileStatus,
        fileName,
    ):
        """intilizing files model items"""
        self.id = id
        self.companyId = companyId
        self.projectId = projectId
        self.fileType = fileType
        # self.fileVersion = fileVersion
        self.fileAmount = fileAmount
        self.createdBy = createdBy
        self.dateCreated = dateCreated
        self.authorizedOrRejectedBy = authorizedOrRejectedBy
        self.dateAuthorizedOrRejected = dateAuthorizedOrRejected
        self.fileStatus = fileStatus
        self.fileName = fileName


class FilesSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "companyId",
            "projectId",
            "fileType",
            # "fileVersion",
            "fileAmount",
            "createdBy",
            "dateCreated",
            "authorizedOrRejectedBy",
            "dateAuthorizedOrRejected",
            "fileStatus",
            "fileName",
        )


file_schema = FilesSchema()
files_schema = FilesSchema(many=True)
