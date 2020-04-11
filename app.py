from flask import Flask, request, jsonify
from exts import db
from models import User
app = Flask(__name__)
app.config['SECRET_KEY'] = 'lllll'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

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
@app.route('/users')
def users():
    u = User.query.all()
    return jsonify(u)

if __name__ == '__main__':
    app.run(debug=True)

