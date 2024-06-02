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

document.getElementById('movie_id').addEventListener('change', function() {
    var selectedMovieId = this.value;
    fetch(`/movie/schedule/${selectedMovieId}`)
        .then(response => response.json())
        .then(data => {
            const scheduleOptions = document.getElementById('schedule_options');
            scheduleOptions.innerHTML = ''; // Clear existing options
            Object.keys(data).forEach(theaterId => {
                const theaterSchedules = data[theaterId];
                const theaterGroup = document.createElement('div');
                theaterGroup.classList.add('theater-group');
                const theaterHeader = document.createElement('h4');
                theaterHeader.textContent = `Theater ${theaterId}`;
                theaterGroup.appendChild(theaterHeader);
                theaterSchedules.forEach(schedule => {
                    const radioOption = document.createElement('input');
                    radioOption.type = 'radio';
                    radioOption.name = 'schedule_id';
                    radioOption.value = schedule.id;
                    radioOption.id = `schedule_${schedule.id}`;

                    const label = document.createElement('label');
                    label.htmlFor = `schedule_${schedule.id}`;
                    label.textContent = `Time: ${schedule.time}`;

                    // Add radio button and label to theater group
                    theaterGroup.appendChild(radioOption);
                    theaterGroup.appendChild(label);

                    // Add event listener to update selected time when radio button is clicked
                    radioOption.addEventListener('change', function() {
                        document.getElementById('selected_time').value = schedule.time;
                    });
                });
                scheduleOptions.appendChild(theaterGroup);
            });
        })
        .catch(error => console.error('Error fetching movie schedule:', error));
});

function updateSchedule(event) {
    event.preventDefault();
    var scheduleId = document.querySelector('input[name="schedule_id"]:checked').value;
    var time = document.getElementById("selected_time").value;

    var updateData = { schedule_id: scheduleId }; // Pastikan schedule_id disertakan dalam data
    if (time) updateData.time = time;

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
    var scheduleId = document.querySelector('input[name="schedule_id"]:checked').value;
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
