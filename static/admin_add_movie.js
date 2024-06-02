
        async function addMovie(event) {
    event.preventDefault();

    const form = document.getElementById('addForm');
    const formData = new FormData(form);

    try {
        const response = await fetch('/add/movie/', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (response.ok) {
            Swal.fire({
                title: 'Success!',
                text: `Movie added successfully with ID: ${result.id}`,
                icon: 'success',
                confirmButtonText: 'OK'
            });
        } else {
            Swal.fire({
                title: 'Error',
                text: result.error,
                icon: 'error',
                confirmButtonText: 'OK'
            });
        }
    } catch (error) {
        Swal.fire({
            title: 'Error',
            text: 'An unexpected error occurred.',
            icon: 'error',
            confirmButtonText: 'OK'
        });
    }
}

document.getElementById('addForm').addEventListener('submit', addMovie);

