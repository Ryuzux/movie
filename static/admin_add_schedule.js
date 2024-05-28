async function addSchedule(event) {
    event.preventDefault();
    
    const movie_id = document.getElementById('movie_id').value;
    const time = document.getElementById('time').value;
    const theater_id = document.getElementById('theater_id').value;
    
    const response = await fetch('/add/schedule/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            movie_id,
            time,
            theater_id
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