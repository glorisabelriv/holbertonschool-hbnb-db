from Model.basemodel import BaseModel
from datab import db

class Country(BaseModel):
    __tablename__ = 'countries'
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(2), nullable=False)
    cities = db.relationship('City', backref='country', lazy=True)


    """ Country class that represents a country with a name and an area code. """
    def __init__(self, name, code, **kwargs):
        """ Initializes the Country with attributes id, name, and area code. """
        super().__init__(**kwargs)
        self.name = name
        self.code = code

    def __str__(self):
        return f"[Country] ({self.id}) {self.to_dict()}"


    def to_dict(self):
        return {
            'name': self.name,
            'code': self.code,
        }
