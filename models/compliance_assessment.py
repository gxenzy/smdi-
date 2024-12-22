from extensions import db

# models/compliance_assessment.py
class ComplianceAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=False)