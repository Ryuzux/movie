document.getElementById("updateForm").addEventListener("submit", function(event) {
    event.preventDefault();
    updateMovie();
});

function updateMovie() {
    var movieId = document.getElementById("movieid").value;
    var movieName = document.getElementById("name").value;
    var movieLaunching = document.getElementById("launching").value;
    var movieCategory = document.getElementById("category_id").value;
    var movieTicketPrice = document.getElementById("ticket_price").value;
    var moviePosterPath = document.getElementById("poster_path").value;

    var updateData = { id: movieId };
    if (movieName) updateData.name = movieName;
    if (movieLaunching) updateData.launching = movieLaunching;
    if (movieCategory) updateData.category_id = movieCategory;
    if (movieTicketPrice) updateData.ticket_price = movieTicketPrice;
    if (moviePosterPath) updateData.poster_path = moviePosterPath;

    fetch('/update/movie/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updateData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            Swal.fire(data.message);
        } else if (data.error) {
            Swal.fire(data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}

function deleteMovie() {
    var movieId = document.getElementById("movieid").value;
    fetch('/update/movie/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: movieId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            Swal.fire(data.message);
        } else if (data.error) {
            Swal.fire(data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}