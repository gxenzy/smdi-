from extensions import db

class ElectricalSystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Add other fields as necessary

    def __repr__(self):
        return f'<ElectricalSystem {self.name}>'