document.addEventListener("DOMContentLoaded", function() {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');

    searchForm.onsubmit = function(event) {
        if (!searchInput.value.trim()) {
            event.preventDefault();
            alert('Search cannot be empty');
        }
    };
});
