from models import app, User, Movie
from movie_manage import *
from reporting import *
from user import *
from topup import *
from werkzeug.security import check_password_hash
from flask import render_template,redirect,session,request,jsonify


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['username'] = user.username
        session['user_id'] = user.id
        session['role'] = user.role
        if user.role == 'admin':
            return jsonify({'success': True, 'redirect_url': '/admin'})
        else:
            return jsonify({'success': True, 'redirect_url': '/home'})
    else:
        return jsonify({'success': False, 'error': 'Invalid username or password'}), 401

    
@app.route('/login', methods=['GET'])
def show_login_page():
    return render_template('login.html')

@app.route('/check_session', methods=['GET'])
def check_session():
    if 'username' in session:
        return jsonify({'logged_in': True, 'role': session['role']})
    else:
        return jsonify({'logged_in': False})
    
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'succes': True})

@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect('/login')
    movies = Movie.query.order_by(Movie.id).all()
    return render_template('admin_dashboard.html', movies=movies)


@app.route('/home')
def home():
    movies = Movie.query.all() 
    return render_template('home.html', movies=movies)

@app.route('/')
def hom():
    movies = Movie.query.all() 
    return render_template('home.html', movies=movies)


if __name__ == '__main__':
    app.run(debug=True)
