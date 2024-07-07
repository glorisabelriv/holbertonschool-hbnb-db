from Model.basemodel import BaseModel
from datab import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):
    __tablename__ = 'users'
    

    email = db.Column(db.String(128), unique=True, nullable=False)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    password = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)


    def __init__(self, email, password, is_admin, password_hash, first_name="", last_name="", **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_admin = is_admin
        self.password_hash = password_hash
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __str__(self):
        return f"[User] ({self.id}) {self.to_dict()}"
    

    def save(self):
        db.session.add(self)
        db.session.commit() 


    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_admin': self.is_admin,
            'password_hash': self.password_hash,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
