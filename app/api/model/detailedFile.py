from app.api.model import db, ma


class DetailedFile(db.Model):
    """
    this creates the  detailedFile model
    """

    __tablename__ = "DetailedFile"

    id = db.Column(db.String(20), primary_key=True)
    companyId = db.Column(db.String(20), db.ForeignKey("Company.id"))
    projectId = db.Column(db.String(20), db.ForeignKey("Project.id"))
    fileType = db.Column(db.String(20), nullable=False)
    urbanLocalTransport = db.Column(db.Float)
    briefingLocalTransport = db.Column(db.Float)
    ruralLocalTransport = db.Column(db.Float)
    periUrbanLocalTransport = db.Column(db.Float)
    interviewerWage = db.Column(db.Float)
    tl_sup_wage = db.Column(db.Float)
    rc_wage = db.Column(db.Float)
    interviewersAllowance = db.Column(db.Float)
    tl_sup_rc_allowance = db.Column(db.Float)
    briefingHighwayTransport = db.Column(db.Float)
    interTownHighwayTransport = db.Column(db.Float)
    interviewerTelephone = db.Column(db.Float)
    tl_sup_rc_telephone = db.Column(db.Float)
    printingCost = db.Column(db.Float)
    covid19Masks = db.Column(db.Float)
    covid19Sanitizers = db.Column(db.Float)
    briefingRefreshments = db.Column(db.Float)
    briefingHallHire = db.Column(db.Float)
    fieldWorkHallHire = db.Column(db.Float)
    totalAmount = db.Column(db.Float)

    def __init__(
        self,
        id,
        companyId,
        projectId,
        fileType,
        urbanLocalTransport,
        briefingLocalTransport,
        ruralLocalTransport,
        periUrbanLocalTransport,
        interviewerWage,
        tl_sup_wage,
        rc_wage,
        interviewersAllowance,
        tl_sup_rc_allowance,
        briefingHighwayTransport,
        interTownHighwayTransport,
        interviewerTelephone,
        tl_sup_rc_telephone,
        printingCost,
        covid19Masks,
        covid19Sanitizers,
        briefingRefreshments,
        briefingHallHire,
        fieldWorkHallHire,
        totalAmount

    ):
        """initializing objects for budget model"""
        self.id = id
        self.companyId = companyId
        self.projectId = projectId
        self.fileType = fileType
        self.urbanLocalTransport = urbanLocalTransport
        self.briefingLocalTransport = briefingLocalTransport
        self.ruralLocalTransport = ruralLocalTransport
        self.periUrbanLocalTransport = periUrbanLocalTransport
        self.interviewerWage = interviewerWage
        self.tl_sup_wage = tl_sup_wage
        self.rc_wage = rc_wage
        self.interviewersAllowance = interviewersAllowance
        self.tl_sup_rc_allowance = tl_sup_rc_allowance
        self.briefingHighwayTransport = briefingHighwayTransport
        self.interTownHighwayTransport = interTownHighwayTransport
        self.interviewerTelephone = interviewerTelephone
        self.tl_sup_rc_telephone = tl_sup_rc_telephone
        self.printingCost = printingCost
        self.covid19Masks = covid19Masks
        self.covid19Sanitizers = covid19Sanitizers
        self.briefingRefreshments = briefingRefreshments
        self.briefingHallHire = briefingHallHire
        self.fieldWorkHallHire = fieldWorkHallHire
        self.totalAmount = totalAmount


class DetailedFileSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "companyId",
            "projectId",
            "fileType",
            "urbanLocalTransport",
            "briefingLocalTransport",
            "ruralLocalTransport",
            "periUrbanLocalTransport",
            "interviewerWage",
            "tl_sup_wage",
            "rc_wage",
            "interviewersAllowance",
            "tl_sup_rc_allowance",
            "briefingHighwayTransport",
            "interTownHighwayTransport",
            "interviewerTelephone",
            "tl_sup_rc_telephone",
            "printingCost",
            "covid19Masks",
            "covid19Sanitizers",
            "briefingRefreshments",
            "briefingHallHire",
            "fieldWorkHallHire",
            "totalAmount"
        )


detailed_file_schema = DetailedFileSchema()
detailed_files_schema = DetailedFileSchema(many=True)
