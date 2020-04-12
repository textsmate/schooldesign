from exts import db,login_manager
from flask_login import UserMixin
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String, nullable=False)
    money = db.Column(db.Integer, default=10000)
    def __repr__(self):
        return f"[{self.name}]"

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class Seller(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"[{self.name}]"
@login_manager.user_loader
def load_user(id):
    return Seller.query.get(id)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    seller = db.relationship('Seller', backref=db.backref('items'))

    def __repr__(self):
        return f"[{self.name}]"

class Shoplist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    userer = db.relationship('User', backref=db.backref('shoplists'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref=db.backref('shoplists'))
    create_time = db.Column(db.DateTime, default=datetime.now)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    user = db.relationship('User', backref=db.backref('comments'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref=db.backref('Comments'))
    create_time = db.Column(db.DateTime, default=datetime.now)