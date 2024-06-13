from flask import request, jsonify,render_template,url_for,redirect,session
from models import app, Movie, Schedule, Category, db, User, Transaction
from datetime import datetime, timedelta,date
from werkzeug.utils import secure_filename
from sqlalchemy import text
import os

app.config['UPLOAD_FOLDER'] = 'D:\python\latihan\mini_project\static\poster'

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def allowed_file(filename):
    if not filename:
        return False
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/movies/<int:movie_id>', methods=['GET'])
def movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404
    
    return jsonify({
        'id': movie.id,
        'name': movie.name,
        'launching': movie.launching,
        'category_id': movie.category_id,
        'ticket_price': movie.ticket_price,
        'poster': movie.poster_path
    }),200


@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get(movie_id)
    schedules = Schedule.query.filter_by(movie_id=movie_id).all()
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    return render_template('movie_detail.html', movie=movie, schedules=schedules)

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movies_list = [{'id': movie.id, 'name': movie.name} for movie in movies]
    return jsonify(movies_list), 200

@app.route('/category', methods=['GET'])
def get_category():
    categories = Category.query.all()
    category_list = [{'id': category.id, 'name': category.name} for category in categories]
    return jsonify(category_list), 200

@app.route('/upcoming')
def upcoming():
    upcoming_movies = Movie.query.filter(~Movie.schedules.any()).all()
    return render_template('upcoming.html', movies=upcoming_movies)

@app.route('/add/movie/', methods=['POST'])
def add_movie():
    
    ensure_dir(app.config['UPLOAD_FOLDER']) 

    if 'name' not in request.form:
        return jsonify({'error': 'name movie must be input'}), 400

    name = request.form['name']
    launching = request.form['launching']
    category_id = request.form['category_id']
    ticket_price = request.form['ticket_price']

    existing_movie = Movie.query.filter_by(name=name).first()
    if existing_movie:
        return jsonify({'error': "the movie currently airing"}), 400

    if 'poster' not in request.files:
        return jsonify({'error': 'poster file must be input'}), 400
    
    poster = request.files['poster']
    if poster.filename == '':
        return jsonify({'error': 'no selected file'}), 400
    
    if poster and allowed_file(poster.filename):
        filename = secure_filename(poster.filename)
        poster.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        poster_path = os.path.join('poster/', filename) 

    if launching:
        try:
            launching_date = datetime.strptime(launching, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'invalid date format, should be YYYY-MM-DD'}), 400
    else:
        launching_date = None 
    
    mov = Movie(
        name=name,
        launching=launching_date,
        category_id=category_id,
        ticket_price=ticket_price,
        poster_path=poster_path
    )
    db.session.add(mov)
    db.session.commit()

    response=({
        'id': mov.id,
        'name': mov.name,
        'category_id': mov.category_id,
        'ticket_price': mov.ticket_price,
        'poster_path': mov.poster_path 
    })
    if launching_date:
        response['launching'] = launching_date.strftime('%Y-%m-%d')
    return jsonify(response), 201



@app.route('/admin/add/movie')
def add_movie_page():
    if  session.get('role') != 'admin':
        return render_template('unauthorized.html'), 404
    return render_template('admin_add_movie.html')



@app.route('/update/movie/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404
    if not allowed_file:
        return jsonify({'error': 'Format file does not support'})

    launching = request.form.get('launching')
    category_id = request.form.get('category_id')
    ticket_price = request.form.get('ticket_price')
    poster_path = request.files.get('poster_path')

    if launching:
        movie.launching = launching
    if category_id:
        movie.category_id = category_id
    if ticket_price:
        movie.ticket_price = ticket_price
    if poster_path:
        poster_filename = secure_filename(poster_path.filename)
        poster_path.save(os.path.join(app.config['UPLOAD_FOLDER'], poster_filename))
        movie.poster_path = os.path.join('poster/', poster_filename)

    try:
        db.session.commit()
        return jsonify({'message': 'Movie updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    
@app.route('/delete/movie/', methods=['DELETE'])
def delete_movie():
    movie_id = request.args.get('id')
    if not movie_id:
        return jsonify({'error': 'Movie id is required in the request'}), 400

    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'Movie deleted successfully'}), 200


@app.route('/admin/update/movie')
def update_movie_page():
    if session.get('role') != 'admin':
        return render_template('unauthorized.html'), 404
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

    threshold_date = datetime.now().date() - timedelta(days=14)

    existing_schedule = Schedule.query.filter(
        Schedule.movie_id == data['movie_id'],
        Schedule.time == data['time'],
        Movie.launching > threshold_date
    ).first()
    
    if existing_schedule:
        return jsonify({
            'error': 'The schedule already exists for a movie airing less than 14 days'
        }), 400

    if 'theater_id' not in data:
        return jsonify({
            'error': 'theater_id must be input'
        }), 400

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
    if session.get('role') != 'admin':
        return render_template('unauthorized.html')
    return render_template('admin_add_schedule.html')


@app.route('/movie/schedule/<int:movie_id>')
def get_movie_schedule(movie_id):
    schedules = Schedule.query.filter_by(movie_id=movie_id).all()
    theater_ids = set(schedule.theater_id for schedule in schedules)
    response_data = {}
    for theater_id in theater_ids:
        response_data[str(theater_id)] = [{
            'id': schedule.id,
            'time': schedule.time.strftime('%H:%M'), 
        } for schedule in schedules if schedule.theater_id == theater_id]
    return jsonify(response_data)


@app.route('/update/schedule/', methods=['PUT', 'DELETE'])
def update_schedule():
    data = request.get_json()
    schedule_id = data.get('schedule_id')
    if not schedule_id:
        return jsonify({
            'error': 'id is required in the request'
        }), 400  
    sch = Schedule.query.get(schedule_id)
    if not sch:
        return jsonify({
            'error': 'Schedule not found'
        }), 404

    if request.method == 'PUT':
        new_time = data.get('time')
        if new_time:
            threshold_date = datetime.now().date() - timedelta(days=14)

            existing_schedule = Schedule.query.filter(
                Schedule.theater_id == sch.theater_id,
                Schedule.time == new_time,
                Movie.launching > threshold_date
            ).join(Movie).first()
            
            if existing_schedule and existing_schedule.id != schedule_id:
                return jsonify({
                    'error': 'Another schedule exists in this theater at the same time for a movie airing less than 14 days.'
                }), 400

            sch.time = new_time
        db.session.commit()

        return jsonify({
            'message': 'Schedule updated successfully',
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
    if session.get('role') != 'admin':
        return render_template('unauthorized.html'), 404
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
            'launching': movie.launching.strftime('%Y-%m-%d') if movie.launching else 'Coming Soon',
            'category': movie.info_category.name,
            'poster_path': movie.poster_path
        }
        for movie in search_results
    ]
    return render_template('search.html', movie_info=movie_info, query=query)


    
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
        max_seat_capacity = schedule.info_theater.total_seat

        if quantity > max_seat_capacity:
            return jsonify({'error': 'The number of requested seats exceeds the maximum capacity of the theater'}), 400
    else:
        return jsonify({'error': 'This movie is no longer active for booking'}), 400

    booked_seat_count_query = text("""
        SELECT COALESCE(SUM(quantity), 0) 
        FROM transaction 
        WHERE schedule_id = :schedule_id AND date = :date
    """)
    booked_seat_count = db.session.execute(
        booked_seat_count_query,
        {'schedule_id': schedule_id, 'date': datetime.today().date()}
    ).scalar()

    available_seat_count = schedule.info_theater.total_seat - booked_seat_count

    if available_seat_count < quantity:
        return jsonify({'error': 'The schedule does not have enough available seats'}), 400

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
