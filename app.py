from flask import Flask, request, jsonify, render_template, redirect
from exts import db, login_manager
from models import User, Seller, Item, Comment, Shoplist
from flask_login import login_user, current_user
import os
import json
basedir = os.path.abspath(os.path.dirname(__file__))+r'\static\uploads\\'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lllll'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
login_manager.init_app(app)
prefix = ''

@app.route('/')
def index():
    return 'design for school'

@app.route(f'{prefix}/signup',methods=['POST'])
def register():
    name = request.form['name']
    password = request.form['password']
    ad = request.form['address']
    ph = int(request.form['phone'])    
    u = User(name=name, password=password, address=ad, phone=ph)
    msg = {
        "code":0,
    }
    if not User.query.filter(User.name==name).first():
        msg['code'] = 1
        db.session.add(u)
        db.session.commit()
    return jsonify(msg)

@app.route(f'{prefix}/signin',methods=['POST'])
def signin():
    name = request.form['name']
    password = request.form['password']
    u = User.query.filter(User.name==name).first()
    msg = {
        "code":0,
        "userid":u.id
    }
    if u:
        if u.password == password:
            msg['code'] = 1
    return jsonify(msg)   

@app.route(f'{prefix}/seller/signup',methods=['GET', 'POST'])
def ssignup():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        f = request.files['avatar']
        avatar = f.filename
        f.save(os.path.join(basedir+avatar))
        u = Seller(name=name, password=password, avatar=avatar)
        db.session.add(u)
        db.session.commit()
        return redirect(f'{prefix}/seller/signin')
        # return redirect('/seller/signin')
    return render_template('signup.html')

@app.route(f'{prefix}/seller/signin',methods=['GET', 'POST'])
def ssignin():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        s = Seller.query.filter(Seller.name==name).first()
        if s.password==password:
            login_user(s)
            # return jsonify({"code":1})
            return redirect(f'{prefix}/seller/items/add')
        # return jsonify({"code":0})
        # return redirect('/seller/signin')
    return render_template('signin.html')

@app.route(f'{prefix}/seller/items/add', methods=['GET', 'POST'])
def itemsadd():
    if request.method == 'POST':
        name = request.form['name']
        price = int(request.form['price'])
        image = request.files['image']
        fname = image.filename
        image.save(os.path.join(basedir+r'item\\'+fname))
        i = Item(name=name, price=price, image=fname, seller=current_user)
        db.session.add(i)
        db.session.commit()
        return render_template('itemsadd.html')
    return render_template('itemsadd.html')

@app.route(f'{prefix}/sellers')
def sellers():
    ss = Seller.query.all()
    seller = []
    for s in ss:
        serial = {
            "id":s.id,
            "avatar":s.avatar,
            "name":s.name,
        }
        seller.append(serial)
    return jsonify(seller)

@app.route(f'{prefix}/seller/<int:id>/items')
def items(id):
    its = Item.query.filter(Item.seller_id==id).all()
    itemss = []
    for it in its:
        serial = {
            "id":it.id,
            "image":it.image,
            "name":it.name
        }
        itemss.append(serial)
    return jsonify(itemss)

@app.route(f'{prefix}/item/<int:id>')
def item(id):
    it = Item.query.filter(Item.id==id).first()
    serial = {
        "id":it.id,
        "image":it.image,
        "name":it.name,
        "price":it.price
    }
    return jsonify(serial)

@app.route(f'{prefix}/item/<int:id>/comment', methods=['POST'])
def comment(id):
    if request.method == 'POST':
        content = request.form['content']
        user_id = int(request.form['uid'])
        c = Comment(content=content, user_id=user_id, item_id=id)
        db.session.add(c)
        db.session.commit()
        return jsonify({
            "code":1
        })

@app.route(f'{prefix}/item/<int:id>/comments')
def get_comment(id):
    cs = Comment.query.filter(Comment.item_id == id)
    comments = []
    for c in cs:
        serial = {
            "id":c.id,
            "name":c.user.name,
            "content":c.content
        }
        comments.append(serial)
    return jsonify(comments)

@app.route(f'{prefix}/buy', methods=['POST'])
def buy():
    if request.method == 'POST':
        data = json.loads(request.get_data(as_text=True))
        for d in data:
            shop = Shoplist(user_id=d['userid'], item_id=d['itemid'])
            db.session.add(shop)
            db.session.commit()
        return jsonify({"code":1})

@app.route(f'{prefix}/lists/<int:id>')
def lists(id):
    u = User.query.filter(User.id==id).first()
    shoplists = Shoplist.query.filter(Shoplist.user_id==u.id)
    items = []
    for s in shoplists:
        item = s.item
        items.append(item)
    itemss = []
    for it in items:
        serial = {
            "id":it.id,
            "image":it.image,
            "name":it.name
        }
        itemss.append(serial)
    return jsonify(itemss)

@app.route(f'{prefix}/users')
def users():
    u = User.query.all()
    return jsonify(u)

if __name__ == '__main__':
    app.run(debug=True)

