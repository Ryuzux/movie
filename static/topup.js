document.getElementById('topup-form').onsubmit = function(event) {
    event.preventDefault();

    const amountInput = document.getElementById('topup-amount');
    const amount = parseInt(amountInput.value);

    if (amount < 5000) {
        alert('Amount cannot be less than Rp 5000');
        amountInput.value = 0;
        return;
    }

    fetch('/topup/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ amount: amount })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
            // Optionally, you can close the modal here
            let modal = bootstrap.Modal.getInstance(document.getElementById('topupModal'));
            modal.hide();
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
};
