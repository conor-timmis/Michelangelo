window.onload = function() {
    var deleteButtons = document.querySelectorAll('input[type=submit]');
    deleteButtons.forEach(function(button) {
        button.onclick = confirmDelete;
    });
};

function confirmDelete() {
    return confirm("Are you sure you want to delete this booking?");
}
