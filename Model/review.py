from Model.basemodel import BaseModel
from datab import db

class Review(BaseModel):
    __tablename__ = 'reviews'

    place_id = db.Column(db.String(60), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    def __init__(self, place_id, user_id, rating, comment, **kwargs):
        super().__init__(**kwargs)
        self.place_id = place_id
        self.rating = rating
        self.comment = comment
        self.user_id = user_id

    def __str__(self):
        return f"[Review] ({self.id}) {self.to_dict()}"


    def to_dict(self):
        return {
            'place_id': self.place_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'comment': self.comment,
        }
