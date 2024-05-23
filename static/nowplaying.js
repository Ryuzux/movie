document.addEventListener('DOMContentLoaded', function () {
    fetch('/list')
        .then(response => response.json())
        .then(data => {
            const moviesList = document.getElementById('movies-list');
            data.forEach(movie => {
                const movieCard = document.createElement('div');
                movieCard.className = 'col-6 col-md-3 mb-4';
                movieCard.innerHTML = `
                    <a href="/movie/${movie.id}" class="text-decoration-none">
                        <img src="${movie.poster_path ? '/static/poster/' + movie.poster_path : '/static/poster/no-image.png'}" class="img-fluid movie-image" alt="${movie.name}">
                        <div class="movie-details mt-2 text-center">
                            <h5>${movie.name}</h5>
                            <p>Ticket Price: ${movie.ticket_price}</p>
                        </div>
                    </a>
                `;
                moviesList.appendChild(movieCard);
            });
        })
        .catch(error => console.error('Error fetching movies:', error));
});