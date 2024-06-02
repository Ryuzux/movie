from flask import request, jsonify,session,redirect,render_template,url_for
from models import *

@app.route('/topup/', methods=['POST'])
def topup():
    data = request.get_json()
    if 'amount' not in data:
        return jsonify({'error': 'amount must be provided'}), 400

    try:
        amount = int(data['amount'])
    except ValueError:
        return jsonify({'error': 'Amount must be an integer'}), 400

    username = session.get('username')
    if not username:
        return jsonify({'error': 'User must be logged in'}), 403

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found or does not match'}), 404

    new_topup = Topup(user_id=user.id, amount=amount, is_confirmed=False)
    db.session.add(new_topup)
    db.session.commit()

    return jsonify({'topup_id': new_topup.id, 'message': 'Top-up request submitted successfully'}), 200


@app.route('/confirm/topup/', methods=['PUT'])
def confirm_topup():
    topup_id = request.get_json('id')
    if not topup_id:
        return jsonify({
            'error': 'Top-up request ID not provided'
            }), 400

    topup = Topup.query.get(topup_id)
    if not topup:
        return jsonify({
            'error': 'Top-up request not found'
            }), 404

    if not topup.is_confirmed:
        topup.is_confirmed = True
        db.session.commit()

        user = User.query.get(topup.user_id)
        user.balance += topup.amount
        db.session.commit()

        return jsonify({
            'topup_id':topup.id,
            'message': 'Top-up request confirmed successfully'
            }), 200
    else:
        return jsonify({
            'topup_id':topup.id,
            'error': 'Top-up request has already been confirmed'
            }), 400
    
@app.route('/unconfirmed/topups/', methods=['GET'])
def get_unconfirmed_topups():
    unconfirmed_topups = Topup.query.filter_by(is_confirmed=False).all()
    topup_data = [{'id': topup.id, 'user_id': topup.user_id, 'amount': topup.amount} for topup in unconfirmed_topups]
    return jsonify({'topups': topup_data}), 200

@app.route('/admin/confirm/topup/', methods=['GET'])
def admin_confirm_topup():
    if session.get('role') != 'admin':
        return render_template('unauthorized.html')
    return render_template('admin_confirm_topup.html')
