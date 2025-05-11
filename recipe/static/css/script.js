function toggleForm() {
    const form = document.getElementById('leaveForm');
    if (form.style.display === 'none' || form.style.display === '') {
        form.style.display = 'block';
    } else {
        form.style.display = 'none';
    }
}

// Check for flash messages and show the popup
window.onload = function() {
    const messages = document.getElementById('flash-messages').dataset.messages;
    if (messages) {
        document.getElementById('popup').classList.add('show');
    }
};

function closePopup() {
    document.getElementById('popup').classList.remove('show');
}
