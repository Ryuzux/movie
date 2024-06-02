        const beliTiketButtons = document.querySelectorAll('.beli-tiket-btn');
        beliTiketButtons.forEach(button => {
            button.addEventListener('click', function() {
                const scheduleId = button.dataset.scheduleId;
                document.getElementById('purchase-form').setAttribute('data-schedule-id', scheduleId);
                $('#purchaseModal').modal('show');
            });
        });

        document.getElementById('purchase-form').addEventListener('submit', function(event) {
            event.preventDefault();
            const scheduleId = this.dataset.scheduleId;
            const quantity = document.getElementById('quantity').value;
            fetch('/purchase_ticket', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ schedule_id: scheduleId, quantity: parseInt(quantity) })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Pembelian Berhasil!',
                        text: 'Tiket Anda berhasil dibeli.'
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
                    text: 'Terjadi kesalahan saat memproses pembelian tiket.'
                });
            });
        });