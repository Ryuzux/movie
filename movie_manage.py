from flask import request, jsonify,render_template,url_for,redirect,session
from models import *
from datetime import datetime, timedelta,date

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get(movie_id)
    schedules = Schedule.query.filter_by(movie_id=movie_id).all()
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    return render_template('movie_detail.html', movie=movie, schedules=schedules)

@app.route('/add/movie/', methods=['POST'])
def add_movie():
    data = request.get_json()
    
    if 'name' not in data:
        return jsonify({'error': 'name movie must be input'})
    
    existing_movie = Movie.query.filter_by(name=data['name']).first()
    if existing_movie:
        return jsonify({'error': "the movie currently airing"})
    
    if 'launching' not in data:
        return jsonify({'error': 'launching date must be input'})
    
    if 'ticket_price' not in data:
        return jsonify({'error': 'ticket price must be input'})
    
    if 'poster_path' not in data:
        return jsonify({'error': 'poster path must be input'})
    
    poster_path = data['poster_path']
    if not poster_path.startswith('poster/'):
        poster_path = f'poster/{poster_path}'
    
    mov = Movie(
        name=data['name'],
        launching=data['launching'],
        category_id=data['category_id'],
        ticket_price=data['ticket_price'],
        poster_path=poster_path  
    )
    db.session.add(mov)
    db.session.commit()
    
    return jsonify({
        'id': mov.id,
        'name': mov.name,
        'launching': mov.launching.strftime('%Y-%m-%d'),
        'category_id': mov.category_id,
        'ticket_price': mov.ticket_price,
        'poster_path': mov.poster_path 
    })

@app.route('/admin/add/movie')
def add_movie_page():
    if 'logged_in' not in session or session.get('role') != 'admin':
        return render_template('unauthorized.html')
    return render_template('admin_add_movie.html')


@app.route('/update/movie/', methods=['PUT', 'DELETE'])
def update_movie():
    data = request.get_json()
    update_id = data.get('id')
    if not update_id:
        return jsonify({'error': 'movie id is required in the request'}), 400

    movie = Movie.query.get(update_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    if request.method == 'PUT':
        if 'name' in data :
            movie.name = data['name']
        if 'launching' in data :
            movie.launching = data['launching']
        if 'category_id' in data :
            movie.category_id = data['category_id']
        if 'ticket_price' in data :
            movie.ticket_price = data['ticket_price']
        if 'poster_path' in data :
            movie.poster_path = f'poster/{data["poster_path"]}'

        db.session.commit()
        return jsonify({'message': 'Movie updated successfully'}), 200

    elif request.method == 'DELETE':
        db.session.delete(movie)
        db.session.commit()
        return jsonify({'message': 'Movie deleted successfully'}), 200

@app.route('/admin/update/movie')
def update_movie_page():
    if 'logged_in' not in session or session.get('role') != 'admin':
        return render_template('unauthorized.html')
    return render_template('admin_update_movie.html')

@app.route('/add/schedule/', methods=['POST'])
def add_schedule():
    data = request.get_json()

    if 'movie_id' not in data or 'time' not in data:
        return jsonify({
            'error': 'movie_id and time must be provided'
            }), 400

    movie_id = data.get('movie_id')
    if not movie_id:
        return jsonify({
            'error': 'movie_id is required in the request'
            }), 400
    
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({
                'error': 'Movie not found'
                }), 404

    existing_schedule = Schedule.query.filter_by(movie_id=data['movie_id'], time=data['time']).first()
    if existing_schedule:
        return jsonify({
            'error': 'The schedule already exists'
            }), 400

    if 'theater_id' not in data:
        return jsonify({
            'error': 'theater_id must be input'
        })

    new_schedule = Schedule(
        movie_id=data['movie_id'],
        time=data['time'],
        theater_id=data['theater_id']
    )

    db.session.add(new_schedule)
    db.session.commit()

    return jsonify({
        'id': new_schedule.id,
        'movie_id': new_schedule.movie_id,
        'name': new_schedule.movie.name,
        'ticket_price': new_schedule.movie.ticket_price,
        'time': new_schedule.time.strftime('%H:%M'),
        'theater_id': new_schedule.theater_id
    }), 201

@app.route('/admin/add/schedule/', methods=['GET'])
def admin_add_schedule():
    if 'logged_in' not in session or session.get('role') != 'admin':
        return render_template('unauthorized.html')
    return render_template('admin_add_schedule.html')


@app.route('/update/schedule/', methods=['PUT','DELETE'])

def update_schedule():
    data = request.get_json()
    update_id = data.get('id')
    if not update_id:
        return jsonify({
            'error': 'id is required in the request'
        })
    sch = Schedule.query.get(update_id)
    if not sch:
        return jsonify({
            'error': 'Schedule not found'
            }), 404
    if request.method == 'PUT':
        if 'id' in data:
            sch.id = data['id']
        if 'movie_id' in data:
            sch.movie_id = data['movie_id']
        if 'time' in data:
            sch.time = data['time']
        if 'theater_id' in data:
            sch.theater_id = data['theater_id']

        db.session.commit()
        return jsonify({
            'id': sch.id,
            'movie_id': sch.movie_id,
            'theater_id': sch.theater_id,
            'name': sch.movie.name,
            'time': sch.time.strftime('%H:%M')
        }), 200
    
    elif request.method == 'DELETE':
        db.session.delete(sch)
        db.session.commit()
        return jsonify({
            'message': 'Schedule deleted successfully'
            }), 200
    
@app.route('/admin/update/schedule/', methods=['GET'])
def admin_update_schedule():
    if 'logged_in' not in session or session.get('role') != 'admin':
        return render_template('unauthorized.html')
    return render_template('admin_update_schedule.html')


@app.route('/nowplaying', methods=['GET'])
def now_playing_page():
    play_date = date.today()
    max_launching_date = play_date - timedelta(days=14)
    active_movies = Movie.query.filter(Movie.launching >= max_launching_date).all()

    movie_info = [{
        'id': movie.id,
        'name': movie.name,
        'category': movie.info_category.name,
        'ticket_price': f'Rp {movie.ticket_price}',
        'poster_path': movie.poster_path,
        'launching': movie.launching.strftime('%Y-%m-%d'),
        'schedules': [{
            'time': schedule.time.strftime('%H:%M'),
            'theater': schedule.info_theater.room if schedule.info_theater else None
        } for schedule in movie.schedules]
    } for movie in active_movies]

    return render_template('nowplaying.html', movies=movie_info)


@app.route('/search/', methods=['GET'])
def search_movie():
    query = request.args.get('query')
    if not query:
        return jsonify({
            'error': 'Query parameter is required'
        }), 400

    name_results = Movie.query.filter(Movie.name.ilike(f"%{query}%")).all()
    category_results = Movie.query.join(Category).filter(Category.name.ilike(f"%{query}%")).all()
    search_results = name_results + category_results
    movie_info = [
        {
            'id': movie.id,
            'name': movie.name,
            'launching': movie.launching.strftime('%Y-%m-%d'),
            'category': movie.info_category.name,
            'poster_path': movie.poster_path
        }
        for movie in search_results
    ]
    return render_template('search.html', movie_info=movie_info, query=query)


@app.route('/buy/ticket', methods=['POST'])
def buy():
    data = request.get_json()
    schedule_id = data.get('schedule_id')

    if not schedule_id:
        return jsonify({'error': 'schedule_id must be provided'}), 400

    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        return jsonify({'error': 'Schedule not found'}), 404

    launching_date = schedule.movie.launching
    max_launching_date = datetime.today().date() - timedelta(days=7)

    if launching_date > max_launching_date:
        available_seat_count = schedule.info_theater.total_seat - Transaction.query.filter_by(schedule_id=schedule_id).filter_by(date=datetime.today().date()).count()
        if available_seat_count <= 0:
            return jsonify({'error': 'The schedule has full booking'}), 400
    else:
        return jsonify({'error': 'This movie is no longer active for booking'}), 400

    ticket_price = schedule.movie.ticket_price
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if user.balance < ticket_price:
        return jsonify({'error': 'Insufficient balance'}), 400

    user.balance -= ticket_price
    new_transaction = Transaction(
        user_id=user.id,
        schedule_id=schedule_id,
        date=datetime.today().date()
    )

    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({'message': 'Ticket purchased successfully'}), 200

    
@app.route('/purchase_ticket', methods=['POST', 'GET'])
def purchase_ticket():
    data = request.get_json()
    schedule_id = data.get('schedule_id')
    quantity = data.get('quantity')
    user_id = session.get('user_id')

    if not schedule_id or not quantity:
        return jsonify({'error': 'Invalid data'}), 400

    if not user_id:
        return jsonify({'error': 'User not logged in'}), 403

    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        return jsonify({'error': 'Schedule not found'}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    launching_date = schedule.movie.launching
    max_launching_date = datetime.today().date() - timedelta(days=14)

    if launching_date > max_launching_date:
        booked_seat_count = db.session.query(db.func.sum(Transaction.quantity)).filter_by(schedule_id=schedule_id).scalar() or 0
        available_seat_count = schedule.info_theater.total_seat - booked_seat_count

        if available_seat_count < quantity:
            return jsonify({'error': 'The schedule has full booking'}), 400
    else:
        return jsonify({'error': 'This movie is no longer active for booking'}), 400

    total_price = schedule.movie.ticket_price * quantity
    if user.balance < total_price:
        return jsonify({'error': 'Insufficient balance'}), 400

    user.balance -= total_price
    new_transaction = Transaction(
        user_id=user.id,
        schedule_id=schedule_id,
        quantity=quantity,
        date=datetime.today().date()
    )

    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'success': True})

