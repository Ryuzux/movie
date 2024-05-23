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
