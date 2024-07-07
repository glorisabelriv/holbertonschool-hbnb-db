from Model.basemodel import BaseModel
from datab import db
from Model.country import Country

class City(BaseModel):
    __tablename__ = 'cities'
    name = db.Column(db.String(128), nullable=False)
    country_code = db.Column(db.String(2), db.ForeignKey('countries.code'), nullable=False)
    places = db.relationship('Place', backref='city', lazy=True)
    
    """ City class that inherits from BaseModel """
    def __init__(self, name, country_code, **kwargs):
        """ Initializes the city with name, country and additional attributes """
        super().__init__(**kwargs)
        self.name = name
        self.country_code = country_code

    def __str__(self):
        return f"[City] ({self.id}) {self.to_dict()}"


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country_code': self.country_code,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
