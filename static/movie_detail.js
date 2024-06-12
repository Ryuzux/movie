document.addEventListener('DOMContentLoaded', function() {
    const buyTicket = document.querySelectorAll('.buy-ticket-btn');
    buyTicket.forEach(button => {
        button.addEventListener('click', function() {
            const scheduleId = button.dataset.scheduleId;
            document.getElementById('purchase-form').setAttribute('data-schedule-id', scheduleId);
            $('#purchaseModal').modal('show');
        });
    });


    document.getElementById('purchase-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const scheduleId = this.dataset.scheduleId;
        const quantityInput = document.getElementById('quantity');
        const quantity = quantityInput.value;
        const quantityInt = parseInt(quantity);

        if (quantityInt < 1) {
            Swal.fire({
                icon: 'error',
                title: 'Buy Ticket Failed',
                text: 'Minimum Buy Ticket 1'
            });
            quantityInput.value = 0;
            return; 
        }

        fetch('/purchase_ticket', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ schedule_id: scheduleId, quantity: quantityInt })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Buy Ticket Success',
                    text: 'Your Ticket has been successfully purchased'
                });
                $('#purchaseModal').modal('hide');
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: data.error
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Something wrong with your purchased ticket'
            });
        });
    });
});
