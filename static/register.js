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
            alert(body.error || body.message);
        } else {
            alert('Registered successfully');
            window.location.href = '/login';
        }
    })
    .catch(error => console.error('Error:', error));
});