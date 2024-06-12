from flask import  jsonify
from models import *
from user import *
from sqlalchemy import create_engine, text


engine = create_engine('postgresql://postgres:1234@localhost/movie')

@app.route('/topmovie', methods=['GET', 'POST'])
def most_popular_movie():
    with engine.connect() as con:
        sql_query = text("""
        SELECT
            m.id,
            m.name,
            m.poster_path,
            m.ticket_price,
            COUNT(t.id) AS ticket
        FROM movie m
        JOIN schedule s ON m.id = s.movie_id
        JOIN transaction t ON s.id = t.schedule_id
        GROUP BY m.id, m.name, m.poster_path, m.ticket_price
        ORDER BY ticket DESC
        LIMIT 5;
        """)

        result = con.execute(sql_query)
        top_movies = [
            {
                "id": row[0],
                "movie": row[1],
                "poster_path": row[2],
                "ticket_price": row[3],
                "ticket_count": row[4]
            } for row in result
        ]
        return render_template('topmovie.html', top_movies=top_movies)


@app.route('/admin/report', methods=['GET'])
def admin_report():
    if session.get('role') != 'admin':
        return render_template('unauthorized.html')
    
    transactions = Transaction.query.all()
    transaction_data = []
    total_sum = 0  

    for transaction in transactions:
        schedule = Schedule.query.get(transaction.schedule_id)
        movie = Movie.query.get(schedule.movie_id) if schedule else None
        ticket_price = movie.ticket_price if movie else 0
        quantity = transaction.quantity or 0  
        total_price = ticket_price * quantity  
        total_sum += total_price  

        transaction_data.append({
            'id': transaction.id,
            'username': transaction.info_user.username,
            'movie': movie.name if movie else "Unknown",  
            'date': transaction.date,
            'quantity': quantity,
            'total_price': f'{total_price:,.0f}'  
        })
    
    total_sum_formatted = f'{total_sum:,.0f}'  
    
    return render_template('admin_report.html', transactions=transaction_data, total_sum=total_sum_formatted)


