document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    
    fetch('/login', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Network response was not ok');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect_url;
        } else {
            alert('Login failed: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while logging in. Please try again later.');
    });
});

// Pengecekan sesi pengguna saat memuat halaman
document.addEventListener('DOMContentLoaded', function() {
    fetch('/check_session', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        if (data.logged_in) {
            if (data.role === 'admin') {
                window.location.href = '/admin';
            } else {
                window.location.href = '/home';
            }
        }
    })
    .catch(error => {
        console.error('Error checking session:', error);
    });
});
