from flask import request, jsonify,session,url_for,redirect,render_template
from models import *
from werkzeug.security import generate_password_hash



@app.route('/register/', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Username and password must be provided'
            }), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({
                'error': 'Username already exists'
            }), 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'message': 'Registered successfully'
        }), 200
    else:
        return render_template('register.html')

@app.route('/update/user', methods=['PUT', 'GET'])
def update_user():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if the user is not logged in

    if request.method == 'GET':
        return render_template('update.html')
    
    elif request.method == 'PUT':
        data = request.get_json()
        current_username = session['username']

        user = User.query.filter_by(username=current_username).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if 'new_username' in data:
            user.username = data['new_username']
            session['username'] = data['new_username']  # Update session username if changed
        
        if 'new_password' in data:
            user.password = generate_password_hash(data['new_password'], method='pbkdf2:sha256', salt_length=16)
        
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200

@app.route('/user')
def user():
    if 'logged_in' in session and session['logged_in']:
        current_user = User.query.filter_by(username=session['username']).first()
        if current_user:
            username = current_user.username
            balance = current_user.balance
            return render_template('profile.html', username=username, balance=balance)
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return redirect(url_for('login'))

# @app.route('/profile')
# def profile():
#     if 'logged_in' in session and session['logged_in']:
#         username = session['username']
#         return render_template('profile.html', username=username)
#     else:
#         return redirect(url_for('login'))