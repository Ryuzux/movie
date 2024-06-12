from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from datetime import timedelta



app = Flask(__name__)

app.config['SECRET_KEY']= 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/movie'
db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db
app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

UPLOAD_FOLDER = 'static/poster'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


Migrate = Migrate(app, db)
Session(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    launching = db.Column(db.Date)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    ticket_price = db.Column(db.Integer, nullable=False)
    schedules = db.relationship('Schedule', back_populates='movie')
    poster_path = db.Column(db.String)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    movies = db.relationship('Movie', backref='info_category', lazy='dynamic')

class Theater(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room = db.Column(db.Integer, unique=True)
    total_seat = db.Column(db.Integer)
    schedules = db.relationship('Schedule', backref='info_theater', lazy='dynamic')

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seat_number = db.Column(db.String)
    seats = db.relationship('Transaction', backref='info_seat', lazy='dynamic')

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    time = db.Column(db.Time, nullable=False)
    movie = db.relationship('Movie', back_populates='schedules')
    transactions = db.relationship('Transaction', backref='info_schedule', lazy='dynamic')
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'))

class Topup(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Integer, default=0)
    is_confirmed = db.Column(db.Boolean, default=False)
    
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)
    date = db.Column(db.Date, default=0)
    quantity = db.Column(db.Integer)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.Integer, default=0)
    role = db.Column(db.String(20), default='user')
    transactions = db.relationship('Transaction', backref='info_user', lazy='dynamic')

    # def admin_required(fn):
    #     @wraps(fn)
    #     def wrapper(*args, **kwargs):
    #         username = request.authorization.username
    #         user = User.query.filter_by(username=username).first()
    #         if user and user.role == "admin":
    #             return fn(*args, **kwargs)
    #         else:
    #             return jsonify({
    #                 "error": "Unauthorized"
    #                 }), 401
    #     return wrapper

    # @staticmethod
    # def admin_or_user_required(fn):
    #     @wraps(fn)
    #     def wrapper(*args, **kwargs):
    #         auth = request.authorization
    #         if not auth or not auth.username or not auth.password:
    #             return jsonify({"error": "Unauthorized"}), 401

    #         current_user = User.query.filter_by(username=auth.username).first()

    #         if not current_user or not check_password_hash(current_user.password, auth.password):
    #             return jsonify({"error": "Unauthorized"}), 401

    #         return fn(current_user=current_user, *args, **kwargs)
        
    #     return wrapper