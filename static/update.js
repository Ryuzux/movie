document.getElementById('update-user-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const username = document.getElementById('user').value.trim();
    const password = document.getElementById('pass').value.trim();
    
    const formData = {
        username: username,
        new_username: username,
        new_password: password
    };
    
    fetch('/update/user', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw err; });
        }
        return response.json();
    })
    .then(data => {
        Swal.fire({
            icon: 'success',
            title: 'Success',
            text: data.message,
        }).then(() => {
            window.location.href = '/user'; 
        });
    })
    .catch(error => {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: error.error || 'Something went wrong!',
        });
    });
});
