from flask import Flask, request, jsonify, render_template, redirect
from exts import db, login_manager
from models import User, Seller, Item
from flask_login import login_user, current_user
import os
basedir = os.path.abspath(os.path.dirname(__file__))+r'\static\uploads\\'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lllll'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
login_manager.init_app(app)
@app.route('/')
def index():
    return 'design for school'

@app.route('/signup',methods=['POST'])
def register():
    name = request.form['name']
    password = request.form['password']
    u = User(name=name, password=password)
    db.session.add(u)
    db.session.commit()
    msg = {
        "code":1
    }
    return jsonify(msg)

@app.route('/signin',methods=['POST'])
def signin():
    name = request.form['name']
    password = request.form['password']
    u = User.query.filter(User.name==name).first()
    msg = {
        "code":0
    }
    if u:
        if u.password == password:
            msg['code'] = 1
    return jsonify(msg)   

@app.route('/seller/signup',methods=['GET', 'POST'])
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
        return jsonify({"code":1})
        # return redirect('/seller/signin')
    return render_template('signup.html')

@app.route('/seller/signin',methods=['GET', 'POST'])
def ssignin():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        s = Seller.query.filter(Seller.name==name).first()
        if s.password==password:
            login_user(s)
            # return jsonify({"code":1})
            return redirect('/seller/items/add')
        # return jsonify({"code":0})
        # return redirect('/seller/signin')
    return render_template('signin.html')

@app.route('/seller/items/add', methods=['GET', 'POST'])
def itemsadd():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        image = request.files['image']
        fname = image.filename
        image.save(os.path.join(basedir+r'item\\'+fname))
        i = Item(name=name, desc=desc, image=fname, seller=current_user)
        db.session.add(i)
        db.session.commit()
        return redirect('/seller/items')
    return render_template('itemsadd.html')

@app.route('/seller/items')
def items():
    return 'test'

@app.route('/users')
def users():
    u = User.query.all()
    return jsonify(u)

if __name__ == '__main__':
    app.run(debug=True)

