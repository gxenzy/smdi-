from extensions import db

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_acceptance = db.Column(db.Float, nullable=False)