from exts import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String, nullable=False)
    money = db.Column(db.Integer, default=10000)
    def __repr__(self):
        return f"[{self.name}]"