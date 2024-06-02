from flask import request, jsonify,render_template,url_for,redirect,session
from models import *
from datetime import datetime, timedelta,date
from werkzeug.utils import secure_filename
import os
app.config['UPLOAD_FOLDER'] = 'D:\python\latihan\mini_project\static\poster'

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


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
    return jsonify(movies_list)

@app.route('/category', methods=['GET'])
def get_category():
    categories = Category.query.all()
    category_list = [{'id': category.id, 'name': category.name} for category in categories]
    return jsonify(category_list)

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
    
    mov = Movie(
        name=name,
        launching=datetime.strptime(launching, '%Y-%m-%d'),
        category_id=category_id,
        ticket_price=ticket_price,
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
    }), 201



@app.route('/admin/add/movie')
def add_movie_page():
    if  session.get('role') != 'admin':
        return render_template('unauthorized.html'), 404
    return render_template('admin_add_movie.html')



@app.route('/update/movie/', methods=['PUT', 'DELETE'])
def update_movie():
    ensure_dir(app.config['UPLOAD_FOLDER']) 

    data = request.form.to_dict() 
    update_id = data.get('id')
    if not update_id:
        return jsonify({'error': 'Movie id is required in the request'}), 400

    movie = Movie.query.get(update_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404

    if request.method == 'PUT':
        if 'name' in data:
            movie.name = data['name']
        if 'launching' in data:
            movie.launching = data['launching']
        if 'category_id' in data:
            movie.category_id = data['category_id']
        if 'ticket_price' in data:
            movie.ticket_price = data['ticket_price']

        if 'poster' in request.files:
            poster = request.files['poster']
            if poster and allowed_file(poster.filename):
                filename = secure_filename(poster.filename)
                poster.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                movie.poster_path = os.path.join('poster/', filename)

        db.session.commit()
        return jsonify({'message': 'Movie updated successfully'}), 200

    elif request.method == 'DELETE':
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
            existing_schedule = Schedule.query.filter_by(
                theater_id=sch.theater_id, time=new_time
            ).first()
            if existing_schedule and existing_schedule.id != schedule_id:
                return jsonify({
                    'error': 'Another schedule exists in this theater at the same time.'
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
            'launching': movie.launching.strftime('%Y-%m-%d'),
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

    booked_seat_count = db.session.query(db.func.sum(Transaction.quantity)).filter_by(schedule_id=schedule_id).filter_by(date=datetime.today().date()).scalar() or 0
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



