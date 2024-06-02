document.addEventListener('DOMContentLoaded', function() {
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
    var moviePoster = document.getElementById("poster_path").files[0];

    if (!movieLaunching && !movieCategory && !movieTicketPrice && !moviePoster) {
        Swal.fire("At least one field must be filled out to update the movie");
        return;
    }

    if (!movieId) {
        Swal.fire("Movie ID is required");
        return;
    }

    var formData = new FormData();
    formData.append('id', movieId);
    if (movieLaunching) formData.append('launching', movieLaunching);
    if (movieCategory) formData.append('category_id', movieCategory);
    if (movieTicketPrice) formData.append('ticket_price', movieTicketPrice);
    if (moviePoster) formData.append('poster', moviePoster);

    fetch('/update/movie/', {
        method: 'PUT',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            Swal.fire(data.message);
        } else if (data.error) {
            Swal.fire(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire("An error occurred");
    });
}
