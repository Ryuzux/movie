document.getElementById("update-movie-btn").onclick = function() {
    window.location.href = "/admin/update/movie";
};

    document.getElementById("update-schedule-btn").onclick = function() {
    window.location.href = "/admin/update/schedule";
};

document.addEventListener("DOMContentLoaded", function() {
    const deleteButtons = document.querySelectorAll(".delete-btn");
    deleteButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            const movieId = this.getAttribute("data-movie-id");
            Swal.fire({
                title: 'Are you sure?',
                text: "You won't be able to revert this!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'delete'
            }).then((result) => {
                if (result.isConfirmed) {
                    deleteMovie(movieId);
                }
            });
        });
    });
    
    function deleteMovie(movieId) {
        fetch(`/delete/movie/?id=${movieId}`, { 
            method: 'DELETE',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            Swal.fire(
                'Deleted!',
                'The movie has been deleted.',
                'success'
            ).then(() => {
                window.location.reload(); 
            });
        })
        .catch(error => {
            console.error('There was an error!', error);
            Swal.fire(
                'Error!',
                'There was an error deleting the movie.',
                'error'
            );
        });
    }
});
