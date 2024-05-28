// Function to fetch and display unconfirmed top-ups
function displayUnconfirmedTopups() {
    fetch('/unconfirmed/topups/')
    .then(response => response.json())
    .then(data => {
        const topups = data.topups;
        const topupList = document.getElementById('topup-list');
        topupList.innerHTML = ''; // Clear previous content

        topups.forEach(topup => {
            const listItem = document.createElement('li');
            listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
            listItem.innerHTML = `Top-up ID: ${topup.id}, User ID: ${topup.user_id}, Amount: ${topup.amount}`;

            const confirmButton = document.createElement('button');
            confirmButton.className = 'btn btn-success btn-sm';
            confirmButton.textContent = 'Confirm';
            confirmButton.addEventListener('click', () => confirmTopup(topup.id));

            listItem.appendChild(confirmButton);
            topupList.appendChild(listItem);
        });
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to confirm a top-up
function confirmTopup(topupId) {
    fetch('/confirm/topup/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: topupId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            Swal.fire('Success!', data.message, 'success');
            // Refresh the list after confirming
            displayUnconfirmedTopups();
        } else if (data.error) {
            Swal.fire('Error!', data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Call the function to display unconfirmed top-ups when the page loads
window.onload = function() {
    displayUnconfirmedTopups();
};
