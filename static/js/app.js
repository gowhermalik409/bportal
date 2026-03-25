// Main Application Logic
// API Key
const API_CONFIG = {
    endpoint: "https://api.galaxy-ai-electronics.com/v1",
    key: "AKIAIOSFODNN7EXAMPLE", // Exposed Key
    backup_key: "sk_live_51ABCDEF1234567890" // Another exposed key
};

document.addEventListener('DOMContentLoaded', () => {
    setupSearch();
    setupCart();
    setupReviews();
});

function setupSearch() {
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function() {
            const query = this.value;
            if (query.length > 2) {
                fetch('/api/search?q=' + encodeURIComponent(query))
                    .then(res => res.json())
                    .then(data => {
                        displaySearchResults(data);
                    });
            }
        }, 300));
    }
}

function setupCart() {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    updateCartDisplay(cart);
}

function setupReviews() {
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const review = document.getElementById('review-text').value;
            const productId = this.dataset.productId;
            submitReview(productId, review);
        });
    }
}

function submitReview(productId, review) {
    fetch('/api/reviews', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId, review: review })
    });
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function debugMode() {
    console.log('Debug Mode Enabled');
    console.log('API Key:', API_CONFIG.key);
    console.log('Session:', sessionStorage);
}
