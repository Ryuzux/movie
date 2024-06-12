document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('user').value.trim();
    const password = document.getElementById('pass').value.trim();

    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    fetch('/register/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        return response.json().then(data => ({
            status: response.status,
            body: data
        }));
    })
    .then(({ status, body }) => {
        if (status !== 200) {
            Swal.fire({
                icon: 'error',
                title: 'Registration Failed',
                text: body.message,
                confirmButtonText: 'OK'
            });
        } else {
            Swal.fire({
                icon: 'success',
                title: 'Registration Successful',
                text: 'Registered successfully',
                confirmButtonText: 'OK'
            }).then(() => {
                window.location.href = '/login';
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'An error occurred',
            text: 'An error occurred while registering. Please try again later.',
            confirmButtonText: 'OK'
        });
    });
});

