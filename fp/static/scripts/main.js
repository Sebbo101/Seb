// app/static/scripts/main.js

document.addEventListener('DOMContentLoaded', function() {
    // Fetch and display reviews dynamically using AJAX or fetch API
    // Example:
    fetch('/api/reviews')
        .then(response => response.json())
        .then(reviews => {
            const reviewsContainer = document.getElementById('reviews-container');

            reviews.forEach(review => {
                const reviewElement = document.createElement('div');
                reviewElement.innerHTML = `<p>${review.comment}</p>`;
                reviewsContainer.appendChild(reviewElement);
            });
        })
        .catch(error => console.error('Error fetching reviews:', error));
});
