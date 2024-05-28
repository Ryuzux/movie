

async function addMovie(event) {
    event.preventDefault();
    
    const name = document.getElementById('name').value;
    const launching = document.getElementById('launching').value;
    const category_id = document.getElementById('category_id').value;
    const ticket_price = document.getElementById('ticket_price').value;
    
    const response = await fetch('/add/movie/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name,
            launching,
            category_id,
            ticket_price
        })
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
            title: 'Error!',
            text: result.error,
            icon: 'error',
            confirmButtonText: 'OK'
        });
    }
}