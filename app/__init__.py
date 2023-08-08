
import sqlalchemy
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from .forms import Register, Signin, Game
import sqlalchemy.exc
from flask_login import login_user, login_required, current_user, LoginManager, UserMixin, logout_user
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String, nullable=False)


@login.user_loader
def user_louder(id):
    return User.query.get(id)


@app.route('/', methods=['GET', 'POST'])
def catalog():
    g = Games.query.all()
    return render_template('catalog.html', data=g, user=current_user)


@app.route('/CsGo', methods=['GET'])
def CsGo():
    return render_template('CsGo.html')


@app.route('/sign in', methods=['GET', 'POST'])
def signin():
    s = Signin()
    if s.validate_on_submit():
        user = s.user.data
        password = s.password.data
        u = User.query.filter_by(name=user).first()
        if u is None or u.password != password:
            return redirect('/log in')
        login_user(u, remember=s.galochka.data)
        return redirect('/')
    return render_template('sign in.html', forms=s)


@app.route('/log in', methods=['GET', 'POST'])
def login():
    r = Register()
    if r.validate_on_submit():
        name = r.user.data
        email = r.email.data
        password = r.password.data

        user = User(name=name, email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return render_template('Log in.html', regist=r, error='user or email not available')
        return redirect('/')

    return render_template('Log in.html', regist=r)


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    return render_template('cart.html')


@app.route('/Admin', methods=['GET', 'POST'])
@login_required
def admin():
    g = Game()
    if request.method == 'POST':
        file = request.files['image']
        file.save(f'app/static/images/{file.filename}')
    if g.validate_on_submit():
        price = g.price.data
        name = g.name.data

        game = Games(price=price, name=name, img=f'/static/images/{file.filename}')
        db.session.add(game)
        db.session.commit()
        return redirect('/')

    return render_template('Admin.html', regist=g)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/log in')
