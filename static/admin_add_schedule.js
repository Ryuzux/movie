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
});

async function addSchedule(event) {
    event.preventDefault();
    
    const movieId = document.getElementById('movie_id').value;
    const selectedTimeInput = document.querySelector('input[name="time"]:checked');
    const time = selectedTimeInput ? selectedTimeInput.value : null;
    const selectedTheaterInput = document.querySelector('input[name="theater_id"]:checked');
    const theaterId = selectedTheaterInput ? selectedTheaterInput.value : null;
    
    if (!time) {
        Swal.fire({
            title: 'Error!',
            text: 'Please select a time.',
            icon: 'error',
            confirmButtonText: 'OK'
        });
        return;
    }
    
    if (!theaterId) {
        Swal.fire({
            title: 'Error!',
            text: 'Please select a theater.',
            icon: 'error',
            confirmButtonText: 'OK'
        });
        return;
    }
    
    const response = await fetch('/add/schedule/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            movie_id: movieId,
            time: time,
            theater_id: theaterId
        })
    });
    
    const result = await response.json();
    if (response.ok) {
        Swal.fire({
            title: 'Success!',
            text: `Schedule added successfully with ID: ${result.id}`,
            icon: 'success',
            confirmButtonText: 'OK'
        });
    } else {
        Swal.fire({
            title: 'Error!',
            text: result.error,
            icon: 'error',
            confirmButtonText: 'OK'
        });
    }
}
