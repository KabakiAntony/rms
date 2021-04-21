from app.api.model import db, ma


class Budget(db.Model):
    """
    this creates the  budget model
    """
    __tablename__ = "Budget"

    id = db.Column(db.String(20), primary_key=True)
    companyId = db.Column(db.String(20), db.ForeignKey('Company.id'))
    projectId = db.Column(db.String(20), db.ForeignKey('Project.id'))
    amount = db.Column(db.Float, nullable=False)
    # fileUrl = db.Column(db.String(256), nullable=False, unique=True)

    def __init__(
        self,
        id,
        companyId,
        projectId,
        amount
        # fileUrl
    ):
        """initializing objects for budget model"""
        self.id = id
        self.companyId = companyId
        self.projectId = projectId
        self.amount = amount
        # self.fileUrl = fileUrl


class BudgetSchema(ma.Schema):
    class Meta:
        fields = ("id", "companyId", "projectId", "amount")
        # fields = (
        #     "id",
        #     "budgetVersion"
        #     "companyId",
        #     "projectId",
        #     "amount",
        #     "fileUrl"
        # )


budget_schema = BudgetSchema()
budgets_schema = BudgetSchema(many=True)
