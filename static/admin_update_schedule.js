

function updateSchedule() {
    var scheduleId = document.getElementById("schedule_id").value;
    var movieId = document.getElementById("movie_id").value;
    var time = document.getElementById("time").value;
    var theaterId = document.getElementById("theater_id").value;

    var updateData = { id: scheduleId };
    if (movieId) updateData.movie_id = movieId;
    if (time) updateData.time = time;
    if (theaterId) updateData.theater_id = theaterId;

    fetch('/update/schedule/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updateData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            Swal.fire({
                title: 'Success!',
                text: `Schedule updated successfully`,
                icon: 'success',
                confirmButtonText: 'OK'
            });
        } else if (data.error) {
            Swal.fire({
                title: 'Error!',
                text: data.error,
                icon: 'error',
                confirmButtonText: 'OK'
            });
        }
    })
    .catch(error => console.error('Error:', error));
}

function deleteSchedule() {
    var scheduleId = document.getElementById("schedule_id").value;
    fetch('/update/schedule/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: scheduleId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            Swal.fire({
                title: 'Success!',
                text: `Schedule deleted successfully`,
                icon: 'success',
                confirmButtonText: 'OK'
            });
        } else if (data.error) {
            Swal.fire({
                title: 'Error!',
                text: data.error,
                icon: 'error',
                confirmButtonText: 'OK'
            });
        }
    })
    .catch(error => console.error('Error:', error));
}