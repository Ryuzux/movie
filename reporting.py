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
    if 'logged_in' not in session or session.get('role') != 'admin':
        return render_template('unauthorized.html')
    
    transactions = Transaction.query.all()
    schedules = Schedule.query.all()  # Ambil semua jadwal dari database
    transaction_data = [
        {
            'id': transaction.id,
            'user_id': transaction.user_id,
            'schedule_id': transaction.schedule_id,
            'date': transaction.date,
            'quantity': transaction.quantity,
            'schedule': Schedule.query.get(transaction.schedule_id)  # Dapatkan objek Schedule untuk setiap transaksi
        }
        for transaction in transactions
    ]
    return render_template('admin_report.html', transactions=transaction_data, schedules=schedules)