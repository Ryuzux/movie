from models import *
from user import *
from movie_manage import *
from reporting import *
from topup import *
from flask import render_template,redirect, url_for

from flask import request, jsonify, session, render_template

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Lakukan proses autentikasi pengguna, misalnya dari database
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # Autentikasi berhasil, simpan informasi pengguna dalam sesi
            session['logged_in'] = True
            session['username'] = user.username
            return redirect('/home')
        else:
            # Autentikasi gagal, kembalikan pesan kesalahan
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)  # Hapus status login dari session
    return redirect(url_for('home'))


@app.route('/home')
def home():
    movies = Movie.query.all()  # Mengambil semua data film dari database
    return render_template('home.html', movies=movies)


if __name__ == '__main__':
    app.run(debug=True)
