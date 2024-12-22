from extensions import db

class EnergyAudit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.String(200), nullable=False)