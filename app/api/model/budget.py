from app.api.model import db, ma


class Budget(db.Model):
    """
    this creates the  budget model
    """
    __tablename__ = "Budget"

    id = db.Column(db.Integer, primary_key=True)
    companyId = db.Column(db.Integer, db.ForeignKey('Company.id'))
    projectId = db.Column(db.Integer, db.ForeignKey('Project.id'))
    amount = db.Column(db.Integer, nullable=False)

    def __init___(self, companyId, projectId, amount):
        """initializing objects for budget model"""
        self.companyId = companyId
        self.projectId = projectId
        self.amount = amount


class BudgetSchema(ma.Schema):
    class Meta:
        fields = ("id", "companyId", "projectId", "amount")


budget_schema = BudgetSchema()
bugets_schema = BudgetSchema(many=True)
