document.addEventListener('DOMContentLoaded', function() {
    function loadMovieInfo(selectedMovieId) {
        fetch(`/movies/${selectedMovieId}`)
            .then(response => response.json())
            .then(movieInfo => {
                const launchingInput = document.getElementById('launching');
                
                if (movieInfo.launching) {
                    const date = new Date(movieInfo.launching);
                    const formattedDate = date.toISOString().split('T')[0];
                    launchingInput.value = formattedDate;
                } else {
                    launchingInput.value = ''; 
                    launchingInput.placeholder = 'mm/dd/yyyy'; 
                }

                document.getElementById('category_id').value = movieInfo.category_id || '';
                document.getElementById('ticket_price').value = movieInfo.ticket_price || '';

                const baseUrl = document.body.getAttribute('data-base-url');
                document.getElementById('poster').src = baseUrl + movieInfo.poster;
            })
            .catch(error => console.error('Error fetching movie info:', error));
    }

    fetch('/movies')
        .then(response => response.json())
        .then(movies => {
            const movieSelect = document.getElementById('movie_id');
            movies.forEach(movie => {
                const option = document.createElement('option');
                option.value = movie.id;
                option.text = movie.name;
                movieSelect.appendChild(option);
            });

            movieSelect.addEventListener('change', function() {
                var selectedMovieId = this.value;
                loadMovieInfo(selectedMovieId);
            });
        });

    fetch('/category')
        .then(response => response.json())
        .then(categories => {
            const categorySelect = document.getElementById('category_id');
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category.id;
                option.text = category.name;
                categorySelect.appendChild(option);
            });
        });
});

document.getElementById("updateForm").addEventListener("submit", function(event) {
    event.preventDefault();
    updateMovie();
});

function updateMovie() {
    var movieId = document.getElementById("movie_id").value;
    var movieLaunching = document.getElementById("launching").value;
    var movieCategory = document.getElementById("category_id").value;
    var movieTicketPrice = document.getElementById("ticket_price").value;
    var moviePosterPath = document.getElementById("poster_path").files[0];

        if (moviePosterPath) {
        var allowedExtensions = ['png', 'jpg', 'jpeg', 'gif', 'webp'];
        var fileExtension = moviePosterPath.name.split('.').pop().toLowerCase();
        if (!allowedExtensions.includes(fileExtension)) {
            Swal.fire('Error', 'Unsupported file format. Allowed formats: ' + allowedExtensions.join(', '), 'error');
            return;
        }
    }
    var formData = new FormData();
    formData.append("launching", movieLaunching);
    formData.append("category_id", movieCategory);
    formData.append("ticket_price", movieTicketPrice);
    formData.append("poster_path", moviePosterPath);

    fetch(`/update/movie/${movieId}`, {
        method: "PUT",
        body: formData
    })
    .then(response => response.json())
    .then(result => {
        Swal.fire('Success', 'Movie updated successfully!', 'success');
    })
    .catch(error => {
        console.error("Error updating movie:", error);
        Swal.fire('Error', 'There was an error updating the movie.', 'error');
    });
}
