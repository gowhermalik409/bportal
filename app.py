from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
import base64
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_sessions'

# ==========================================
# 1. DATABASE SIMULATION
# ==========================================

PRODUCTS = [
    {
        'id': 1,
        'name': 'Galaxy S25 Ultra',
        'category': 'Smartphones',
        'price': 1299.99,
        'description': 'The most powerful Galaxy smartphone ever. 200MP camera, Snapdragon 8 Gen 4, 6.8" QHD+ display.',
        'image': 'https://via.placeholder.com/400x300/1a1a2e/ffffff?text=Galaxy+S25+Ultra',
        'stock': 50,
        'rating': 4.8,
        'reviews': []
    },
    {
        'id': 2,
        'name': 'Galaxy Watch 7',
        'category': 'Wearables',
        'price': 399.99,
        'description': 'Advanced health monitoring, GPS, LTE connectivity, and 3-day battery life.',
        'image': 'https://via.placeholder.com/400x300/16213e/ffffff?text=Galaxy+Watch+7',
        'stock': 100,
        'rating': 4.6,
        'reviews': []
    },
    {
        'id': 3,
        'name': 'Galaxy Buds 3 Pro',
        'category': 'Audio',
        'price': 229.99,
        'description': 'Premium noise-cancelling earbuds with 360-degree audio and 8-hour battery life.',
        'image': 'https://via.placeholder.com/400x300/0f3460/ffffff?text=Galaxy+Buds+3+Pro',
        'stock': 150,
        'rating': 4.7,
        'reviews': []
    },
    {
        'id': 4,
        'name': 'Galaxy Tab S10',
        'category': 'Tablets',
        'price': 899.99,
        'description': '14.6" AMOLED display, S Pen included, perfect for productivity and creativity.',
        'image': 'https://via.placeholder.com/400x300/533483/ffffff?text=Galaxy+Tab+S10',
        'stock': 75,
        'rating': 4.5,
        'reviews': []
    },
    {
        'id': 5,
        'name': 'Galaxy Book 4 Pro',
        'category': 'Laptops',
        'price': 1599.99,
        'description': '16" Dynamic AMOLED 2X display, Intel Core i9, 32GB RAM, 1TB SSD.',
        'image': 'https://via.placeholder.com/400x300/e94560/ffffff?text=Galaxy+Book+4+Pro',
        'stock': 30,
        'rating': 4.4,
        'reviews': []
    },
    {
        'id': 6,
        'name': 'Galaxy Z Fold 6',
        'category': 'Smartphones',
        'price': 1799.99,
        'description': 'Revolutionary foldable smartphone with 7.6" main display and multitasking features.',
        'image': 'https://via.placeholder.com/400x300/0f4c75/ffffff?text=Galaxy+Z+Fold+6',
        'stock': 25,
        'rating': 4.9,
        'reviews': []
    }
]

CATEGORIES = ['Smartphones', 'Wearables', 'Audio', 'Tablets', 'Laptops']

# Store contact form submissions (simulated database)
CONTACT_SUBMISSIONS = []

# Store registered users (simulated database)
USERS = {
    'user': {'password': 'user123', 'email': 'john.doe@example.com', 'is_admin': False},
    'admin': {'password': 'admin123', 'email': 'admin@galaxyelectronics.com', 'is_admin': True}
}

# Store user orders (simulated database)
USER_ORDERS = {}

# ==========================================
# 2. STATIC FILE CONTENTS
# ==========================================

# VULNERABLE: Hardcoded API Key
APP_JS_CONTENT = """
// Main Application Logic
// VULNERABLE: Hardcoded API Key in clear text
const API_CONFIG = {
    endpoint: "https://api.galaxy-electronics.com/v1",
    key: "AKIAIOSFODNN7EXAMPLE", // Exposed Key
    backup_key: "sk_live_51ABCDEF1234567890" // Another exposed key
};

// VULNERABLE: PII in client-side storage
document.addEventListener('DOMContentLoaded', () => {
    // Store user data in localStorage (vulnerable)
    if (sessionStorage.getItem('user_id')) {
        const userId = sessionStorage.getItem('user_id');
        console.log('User ID:', userId);
    }
    
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
                // VULNERABLE: Search API call without proper validation
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
    // VULNERABLE: Cart data stored in localStorage (can be manipulated)
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
            
            // VULNERABLE: XSS - User input directly inserted
            submitReview(productId, review);
        });
    }
}

function submitReview(productId, review) {
    // VULNERABLE: No sanitization of user input
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

// VULNERABLE: Debug function exposed
function debugMode() {
    console.log('Debug Mode Enabled');
    console.log('API Key:', API_CONFIG.key);
    console.log('Session:', sessionStorage);
}
"""

# ==========================================
# 3. CSS STYLING
# ==========================================

CUSTOM_CSS = """
:root {
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --secondary: #64748b;
    --success: #22c55e;
    --warning: #f59e0b;
    --danger: #ef4444;
    --dark: #0f172a;
    --light: #f8fafc;
    --white: #ffffff;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--light);
    color: var(--dark);
    line-height: 1.6;
}

/* Navigation */
.navbar {
    background-color: var(--dark);
    color: var(--white);
    padding: 1rem 2rem;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: var(--shadow);
}

.navbar-container {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.navbar-brand {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--white);
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.navbar-brand span {
    color: var(--primary);
}

.navbar-links {
    display: flex;
    gap: 2rem;
    align-items: center;
}

.navbar-links a {
    color: var(--white);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s;
}

.navbar-links a:hover {
    color: var(--primary);
}

.navbar-search {
    display: flex;
    gap: 0.5rem;
}

.navbar-search input {
    padding: 0.5rem 1rem;
    border: 1px solid #334155;
    border-radius: 4px;
    background-color: #1e293b;
    color: var(--white);
    width: 300px;
}

.navbar-search button {
    padding: 0.5rem 1.5rem;
    background-color: var(--primary);
    color: var(--white);
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 600;
}

.navbar-search button:hover {
    background-color: var(--primary-dark);
}

.cart-icon {
    position: relative;
    cursor: pointer;
}

.cart-badge {
    position: absolute;
    top: -8px;
    right: -8px;
    background-color: var(--danger);
    color: var(--white);
    border-radius: 50%;
    padding: 2px 6px;
    font-size: 0.75rem;
    font-weight: bold;
}

/* Container */
.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, var(--dark) 0%, var(--primary-dark) 100%);
    color: var(--white);
    padding: 4rem 2rem;
    text-align: center;
    margin-bottom: 3rem;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.25rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
}

.btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    transition: all 0.3s;
}

.btn-primary {
    background-color: var(--primary);
    color: var(--white);
}

.btn-primary:hover {
    background-color: var(--primary-dark);
}

.btn-secondary {
    background-color: var(--white);
    color: var(--dark);
}

.btn-secondary:hover {
    background-color: var(--light);
}

.btn-danger {
    background-color: var(--danger);
    color: var(--white);
}

.btn-success {
    background-color: var(--success);
    color: var(--white);
}

/* Products Grid */
.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-bottom: 3rem;
}

.product-card {
    background: var(--white);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: transform 0.3s, box-shadow 0.3s;
    cursor: pointer;
}

.product-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}

.product-image {
    width: 100%;
    height: 250px;
    object-fit: cover;
    background-color: #f1f5f9;
}

.product-info {
    padding: 1.5rem;
}

.product-category {
    color: var(--secondary);
    font-size: 0.875rem;
    margin-bottom: 0.5rem;
}

.product-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--dark);
}

.product-description {
    color: var(--secondary);
    font-size: 0.875rem;
    margin-bottom: 1rem;
    line-height: 1.5;
}

.product-price {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary);
    margin-bottom: 1rem;
}

.product-rating {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.stars {
    color: var(--warning);
}

.product-actions {
    display: flex;
    gap: 0.5rem;
}

/* Categories */
.categories {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.category-badge {
    padding: 0.5rem 1rem;
    background-color: var(--white);
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.3s;
}

.category-badge:hover, .category-badge.active {
    background-color: var(--primary);
    color: var(--white);
    border-color: var(--primary);
}

/* Forms */
.form-container {
    max-width: 500px;
    margin: 0 auto;
    background: var(--white);
    padding: 2rem;
    border-radius: 12px;
    box-shadow: var(--shadow);
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: var(--dark);
}

.form-group input,
.form-group textarea,
.form-group select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    font-size: 1rem;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--primary);
}

/* Alerts */
.alert {
    padding: 1rem;
    border-radius: 6px;
    margin-bottom: 1rem;
}

.alert-success {
    background-color: #dcfce7;
    color: #166534;
    border: 1px solid #86efac;
}

.alert-danger {
    background-color: #fee2e2;
    color: #991b1b;
    border: 1px solid #fca5a5;
}

.alert-info {
    background-color: #dbeafe;
    color: #1e40af;
    border: 1px solid #93c5fd;
}

/* Admin Tables */
.admin-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
}

.admin-table th,
.admin-table td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid #e2e8f0;
}

.admin-table th {
    background-color: var(--light);
    font-weight: 600;
}

.admin-table tr:hover {
    background-color: #f8fafc;
}

/* Admin Badge */
.admin-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    background-color: var(--danger);
    color: var(--white);
    font-size: 0.75rem;
    font-weight: bold;
    margin-left: 0.5rem;
}

/* Footer */
.footer {
    background-color: var(--dark);
    color: var(--white);
    padding: 3rem 2rem;
    margin-top: 4rem;
}

.footer-container {
    max-width: 1400px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}

.footer-section h3 {
    margin-bottom: 1rem;
    color: var(--primary);
}

.footer-section a {
    color: #94a3b8;
    text-decoration: none;
    display: block;
    margin-bottom: 0.5rem;
}

.footer-section a:hover {
    color: var(--white);
}

.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid #334155;
    margin-top: 2rem;
    color: #94a3b8;
}

/* Responsive */
@media (max-width: 768px) {
    .navbar-links {
        display: none;
    }
    
    .hero h1 {
        font-size: 2rem;
    }
    
    .products-grid {
        grid-template-columns: 1fr;
    }
}
"""

# ==========================================
# 4. HTML TEMPLATES
# ==========================================

BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Galaxy Electronics - Premium Tech Store{% endblock %}</title>
    <link rel="stylesheet" href="/static/style.css">
    <!-- VULNERABLE: Outdated library references -->
    <!-- jQuery v3.6.0 (Known vulnerabilities) -->
    <!-- Bootstrap v4.6.0 (Outdated) -->
</head>
<body>
    <nav class="navbar">
        <div class="navbar-container">
            <a href="/" class="navbar-brand">
                <span>Galaxy</span> Electronics
            </a>
            
            <div class="navbar-links">
                <a href="/">Home</a>
                <a href="/products">Products</a>
                <a href="/about">About</a>
                <a href="/contact">Contact</a>
                {% if session.get('logged_in') %}
                    <a href="/dashboard">Dashboard</a>
                    <a href="/orders">My Orders</a>
                    {% if session.get('is_admin') %}
                        <a href="/admin">Admin Portal</a>
                    {% endif %}
                    <a href="/logout">Logout</a>
                {% else %}
                    <a href="/login">Login</a>
                    <a href="/register">Register</a>
                {% endif %}
            </div>
            
            <div class="navbar-search">
                <form action="/search" method="GET" style="display:flex; gap:0.5rem;">
                    <input type="text" id="search-input" name="q" placeholder="Search products..." value="{{ search_query }}">
                    <button type="submit">Search</button>
                </form>
            </div>
            
            <div class="cart-icon" onclick="window.location.href='/cart'">
                🛒
                <span class="cart-badge" id="cart-count">0</span>
            </div>
        </div>
    </nav>

    {% block content %}{% endblock %}

    <footer class="footer">
        <div class="footer-container">
            <div class="footer-section">
                <h3>About Us</h3>
                <p>Premium electronics store with the latest technology products.</p>
            </div>
            <div class="footer-section">
                <h3>Quick Links</h3>
                <a href="/products">Products</a>
                <a href="/about">About</a>
                <a href="/contact">Contact</a>
                <a href="/faq">FAQ</a>
            </div>
            <div class="footer-section">
                <h3>Customer Service</h3>
                <a href="/shipping">Shipping Info</a>
                <a href="/returns">Returns</a>
                <a href="/support">Support</a>
            </div>
            <div class="footer-section">
                <h3>Contact</h3>
                <p>Email: support@galaxyelectronics.com</p>
                <p>Phone: 1-800-GALAXY</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 Galaxy Electronics. All rights reserved.</p>
        </div>
    </footer>

    <script src="/static/app.js"></script>
</body>
</html>
"""

HOME_PAGE = BASE_LAYOUT.replace("{% block title %}Galaxy Electronics - Premium Tech Store{% endblock %}", "Galaxy Electronics - Home").replace("{% block content %}{% endblock %}", """
<div class="hero">
    <h1>Welcome to Galaxy Electronics</h1>
    <p>Discover the latest technology products at unbeatable prices</p>
    <div class="hero-buttons">
        <a href="/products" class="btn btn-primary">Shop Now</a>
        <a href="/about" class="btn btn-secondary">Learn More</a>
    </div>
</div>

<div class="container">
    <h2 style="text-align: center; margin-bottom: 2rem;">Featured Products</h2>
    <div class="products-grid">
        {% for product in products[:3] %}
        <div class="product-card" onclick="window.location.href='/product/{{ product.id }}'">
            <img src="{{ product.image }}" alt="{{ product.name }}" class="product-image">
            <div class="product-info">
                <div class="product-category">{{ product.category }}</div>
                <h3 class="product-title">{{ product.name }}</h3>
                <p class="product-description">{{ product.description[:100] }}...</p>
                <div class="product-price">${{ product.price }}</div>
                <div class="product-rating">
                    <span class="stars">★★★★☆</span>
                    <span>{{ product.rating }}</span>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
""")

PRODUCTS_PAGE = BASE_LAYOUT.replace("{% block title %}Galaxy Electronics - Premium Tech Store{% endblock %}", "Galaxy Electronics - Products").replace("{% block content %}{% endblock %}", """
<div class="container">
    <div style="margin-bottom: 2rem;">
        <h1>All Products</h1>
        <div class="categories">
            <a href="/products" class="category-badge {% if not category %}active{% endif %}">All</a>
            {% for cat in categories %}
            <a href="/products?category={{ cat }}" class="category-badge {% if category == cat %}active{% endif %}">{{ cat }}</a>
            {% endfor %}
        </div>
    </div>
    
    <div class="products-grid">
        {% for product in products %}
        <div class="product-card" onclick="window.location.href='/product/{{ product.id }}'">
            <img src="{{ product.image }}" alt="{{ product.name }}" class="product-image">
            <div class="product-info">
                <div class="product-category">{{ product.category }}</div>
                <h3 class="product-title">{{ product.name }}</h3>
                <p class="product-description">{{ product.description }}</p>
                <div class="product-price">${{ product.price }}</div>
                <div class="product-rating">
                    <span class="stars">★★★★☆</span>
                    <span>{{ product.rating }}</span>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
""")

PRODUCT_DETAIL_PAGE = BASE_LAYOUT.replace("{% block title %}Galaxy Electronics - Premium Tech Store{% endblock %}", "{{ product.name }} - Galaxy Electronics").replace("{% block content %}{% endblock %}", """
<div class="container">
    <div style="margin-bottom: 1rem;">
        <a href="/products" style="color: var(--primary); text-decoration: none;">&larr; Back to Products</a>
    </div>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; margin-bottom: 3rem;">
        <div>
            <img src="{{ product.image }}" alt="{{ product.name }}" style="width: 100%; border-radius: 12px; box-shadow: var(--shadow);">
        </div>
        <div>
            <div class="product-category">{{ product.category }}</div>
            <h1 style="font-size: 2.5rem; margin: 0.5rem 0;">{{ product.name }}</h1>
            <div style="margin: 1rem 0;">
                <span class="stars">★★★★☆</span>
                <span>{{ product.rating }} rating</span>
            </div>
            <div class="product-price" style="font-size: 2rem; margin: 1rem 0;">${{ product.price }}</div>
            <p style="color: var(--secondary); margin-bottom: 1.5rem;">{{ product.description }}</p>
            <div style="margin-bottom: 1.5rem;">
                <strong>Stock:</strong> {{ product.stock }} available
            </div>
            <div class="product-actions">
                <a href="/cart/add/{{ product.id }}" class="btn btn-primary" style="flex: 1; text-align: center; padding: 1rem 2rem;">Add to Cart</a>
            </div>
        </div>
    </div>
    
    <div style="margin-top: 3rem;">
        <h2>Customer Reviews</h2>
        {% if product.reviews %}
            {% for review in product.reviews %}
            <div style="background: var(--white); padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem; box-shadow: var(--shadow);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <strong>{{ review.user }}</strong>
                    <span style="color: var(--secondary);">{{ review.date }}</span>
                </div>
                <!-- VULNERABLE: XSS - User input directly rendered -->
                <div>{{ review.text|safe }}</div>
            </div>
            {% endfor %}
        {% else %}
            <p style="color: var(--secondary);">No reviews yet. Be the first to review!</p>
        {% endif %}
        
        {% if session.get('logged_in') %}
        <form id="review-form" data-product-id="{{ product.id }}" style="margin-top: 2rem;">
            <h3>Write a Review</h3>
            <textarea id="review-text" placeholder="Share your experience..." style="width: 100%; padding: 1rem; border: 1px solid #e2e8f0; border-radius: 6px; min-height: 100px;"></textarea>
            <button type="submit" class="btn btn-primary" style="margin-top: 1rem;">Submit Review</button>
        </form>
        {% else %}
        <p style="margin-top: 1rem;"><a href="/login">Login</a> to write a review.</p>
        {% endif %}
    </div>
</div>
""")

SEARCH_RESULTS_PAGE = BASE_LAYOUT.replace("{% block title %}Galaxy Electronics - Premium Tech Store{% endblock %}", "Search Results - Galaxy Electronics").replace("{% block content %}{% endblock %}", """
<div class="container">
    <div style="margin-bottom: 1rem;">
        <a href="/products" style="color: var(--primary); text-decoration: none;">&larr; Back to Products</a>
    </div>
    
    <h1>Search Results</h1>
    
    {% if query %}
    <div class="alert alert-info">
        You searched for: <strong>{{ query|safe }}</strong>
    </div>
    {% endif %}
    
    {% if results %}
        <div class="products-grid">
            {% for product in results %}
            <div class="product-card" onclick="window.location.href='/product/{{ product.id }}'">
                <img src="{{ product.image }}" alt="{{ product.name }}" class="product-image">
                <div class="product-info">
                    <div class="product-category">{{ product.category }}</div>
                    <h3 class="product-title">{{ product.name }}</h3>
                    <p class="product-description">{{ product.description }}</p>
                    <div class="product-price">${{ product.price }}</div>
                </div>
            </div>
            {% endfor %}
        </div>
    {% else %}
        <div style="text-align: center; padding: 3rem; background: var(--white); border-radius: 8px;">
            <h3>No results found</h3>
            <p style="color: var(--secondary);">Try searching for: Galaxy S25, Watch, Buds, Tablet</p>
        </div>
    {% endif %}
</div>
""")

LOGIN_PAGE = BASE_LAYOUT.replace("{% block title %}Galaxy Electronics - Premium Tech Store{% endblock %}", "Login - Galaxy Electronics").replace("{% block content %}{% endblock %}", """
<div class="container">
    <div class="form-container">
        <h1 style="text-align: center; margin-bottom: 2rem;">Login</h1>
        
        {% if error %}
        <div class="alert alert-danger">{{ error }}</div>
        {% endif %}
        
        <form action="/login" method="POST">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" placeholder="Enter your username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Enter your password" required>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;">Login</button>
        </form>
        
        <div style="margin-top: 1rem; text-align: center;">
            <p>Don't have an account? <a href="/register" style="color: var(--primary);">Register</a></p>
        </div>
    </div>
</div>
""")

REGISTER_PAGE = BASE_LAYOUT.replace("{% block title %}Galaxy Electronics - Premium Tech Store{% endblock %}", "Register - Galaxy Electronics").replace("{% block content %}{% endblock %}", """
<div class="container">
    <div class="form-container">
        <h1 style="text-align: center; margin-bottom: 2rem;">Create Account</h1>
        
        {% if error %}
        <div class="alert alert-danger">{{ error }}</div>
        {% endif %}
        
        {% if success %}
        <div class="alert alert-success">{{ success }}</div>
        {% endif %}
        
        <form action="/register" method="POST">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" placeholder="Choose a username" required>
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" placeholder="Enter your email" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Choose a password" required>
            </div>
            <div class="form-group">
                <label for="confirm_password">Confirm Password</label>
                <input type="password" id="confirm_password" name="confirm_password" placeholder="Confirm your password" required>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%;">Create Account</button>
        </form>
        
        <div style="margin-top: 1rem; text-align: center;">
            <p>Already have an account? <a href="/login" style="color: var(--primary);">Login</a></p>
        </div>
    </div>
</div>
""")

DASHBOARD_PAGE = BASE_LAYOUT.replace("{% block title %}Galaxy Electronics - Premium Tech Store{% endblock %}", "Dashboard - Galaxy Electronics").replace("{% block content %}{% endblock %}", """
<div class="container">
    <h1 style="margin-bottom: 2rem;">Welcome, {{ session.get('username', 'User') }}!</h1>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 3rem;">
        <div style="background: var(--white); padding: 2rem; border-radius: 8px; box-shadow: var(--shadow); text-align: center;">
            <h3 style="color: var(--primary);">Total Orders</h3>
            <p style="font-size: 2rem; font-weight: bold;">{{ order_count }}</p>
        </div>
        <div style="background: var(--white); padding: 2rem; border-radius: 8px; box-shadow: var(--shadow); text-align: center;">
            <h3 style="color: var(--success);">Total Spent</h3>
            <p style="font-size: 2rem; font-weight: bold;">${{ total_spent }}</p>
        </div>
        <div style="background: var(--white); padding: 2rem; border-radius: 8px; box-shadow: var(--shadow); text-align: center;">
            <h3 style="color: var(--warning);">Cart Items</h3>
            <p style="font-size: 2rem; font-weight: bold;">{{ cart_count }}</p>
        </div>
    </div>
    
    <div style="background: var(--white); padding: 2rem; border-radius: 8px; box-shadow: var(--shadow); margin-bottom: 2rem;">
        <h2 style="margin-bottom: 1rem;">Recent Orders</h2>
        {% if recent_orders %}
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Date</th>
                        <th>Total</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for order in recent_orders %}
                    <tr>
                        <td>#{{ order.id }}</td>
                        <td>{{ order.date }}</td>
                        <td>${{ order.total }}</td>
                        <td><span style="padding: 0.25rem 0.75rem; border-radius: 20px; background: #dcfce7; color: #166534;">{{ order.status }}</span></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <div style="margin-top: 1rem;">
                <a href="/orders" class="btn btn-secondary">View All Orders</a>
            </div>
        {% else %}
            <p style="color: var(--secondary);">No orders yet.</p>
        {% endif %}
    </div>
</div>
""")

ORDERS_PAGE = BASE_LAYOUT.replace("{% block title %}Galaxy Electronics - Premium Tech Store{% endblock %}", "My Orders - Galaxy Electronics").replace("{% block content %}{% endblock %}", """
<div class="container">
    <div style="margin-bottom: 1rem;">
        <a href="/dashboard" style="color: var(--primary); text-decoration: none;">&larr; Back to Dashboard</a>
    </div>
    
    <h1 style="margin-bottom: 2rem;">My Orders</h1>
    
    <div style="background: var(--white); padding: 2rem; border-radius: 8px; box-shadow: var(--shadow);">
        {% if orders %}
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Date</th>
                        <th>Items</th>
                        <th>Total</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for order in orders %}
                    <tr>
                        <td>#{{ order.id }}</td>
                        <td>{{ order.date }}</td>
                        <td>{{ order.items }}</td>
                        <td>${{ order.total }}</td>
                        <td><span style="padding: 0.25rem 0.75rem; border-radius: 20px; background: #dcfce7; color: #166534;">{{ order.status }}</span></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% else %}
            <p style="color: var(--secondary);">No orders yet. Start shopping!</p>
        {% endif %}
    </div>
</div>
""")

ADMIN_PAGE = BASE_LAYOUT.replace("{% block title %}Galaxy Electronics - Premium Tech Store{% endblock %}", "Admin Portal - Galaxy Electronics").replace("{% block content %}{% endblock %}", """
<div class="container">
    <h1 style="margin-bottom: 2rem;">Admin Portal <span class="admin-badge">ADMIN</span></h1>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 3rem;">
        <div style="background: var(--white); padding: 2rem; border-radius: 8px; box-shadow: var(--shadow); text-align: center;">
            <h3 style="color: var(--primary);">Total Users</h3>
            <p style="font-size: 2rem; font-weight: bold;">{{ total_users }}</p>
        </div>
        <div style="background: var(--white); padding: 2rem; border-radius: 8px; box-shadow: var(--shadow); text-align: center;">
            <h3 style="color: var(--success);">Total Orders</h3>
            <p style="font-size: 2rem; font-weight: bold;">{{ total_orders }}</p>
        </div>
        <div style="background: var(--white); padding: 2rem; border-radius: 8px; box-shadow: var(--shadow); text-align: center;">
            <h3 style="color: var(--warning);">Contact Messages</h3>
            <p style="font-size: 2rem; font-weight: bold;">{{ total_contacts }}</p>
        </div>
        <div style="background: var(--white); padding: 2rem; border-radius: 8px; box-shadow: var(--shadow); text-align: center;">
            <h3 style="color: var(--danger);">Revenue</h3>
            <p style="font-size: 2rem; font-weight: bold;">${{ total_revenue }}</p>
        </div>
    </div>
    
    <div style="background: var(--white); padding: 2rem; border-radius: 8px; box-shadow: var(--shadow); margin-bottom: 2rem;">
        <h2 style="margin-bottom: 1rem;">Contact Form Submissions</h2>
        <p style="color: var(--secondary); margin-bottom: 1rem;">View and manage customer inquiries and feedback.</p>
        
        {% if contact_submissions %}
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Date</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Subject</th>
                        <th>Message</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for submission in contact_submissions %}
                    <tr>
                        <td>{{ submission.id }}</td>
                        <td>{{ submission.date }}</td>
                        <td>{{ submission.name|safe }}</td>
                        <td>{{ submission.email }}</td>
                        <td>{{ submission.subject|safe }}</td>
                        <td>{{ submission.message[:100]|safe }}...</td>
                        <td>
                            <span style="padding: 0.25rem 0.75rem; border-radius: 20px; background: #dbeafe; color: #1e40af;">{{ submission.status }}</span>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% else %}
            <p style="color: var(--secondary);">No contact submissions yet.</p>
        {% endif %}
    </div>
    
    <div style="background: var(--white); padding: 2rem; border-radius: 8px; box-shadow: var(--shadow);">
        <h2 style="margin-bottom: 1rem;">Recent Orders</h2>
        
        {% if all_orders %}
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>User</th>
                        <th>Date</th>
                        <th>Total</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for order in all_orders %}
                    <tr>
                        <td>#{{ order.id }}</td>
                        <td>{{ order.user }}</td>
                        <td>{{ order.date }}</td>
                        <td>${{ order.total }}</td>
                        <td><span style="padding: 0.25rem 0.75rem; border-radius: 20px; background: #dcfce7; color: #166534;">{{ order.status }}</span></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% else %}
            <p style="color: var(--secondary);">No orders yet.</p>
        {% endif %}
    </div>
</div>
""")

CART_PAGE = BASE_LAYOUT.replace("{% block title %}Galaxy Electronics - Premium Tech Store{% endblock %}", "Shopping Cart - Galaxy Electronics").replace("{% block content %}{% endblock %}", """
<div class="container">
    <h1 style="margin-bottom: 2rem;">Shopping Cart</h1>
    
    {% if cart_items %}
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem;">
            <div>
                {% for item in cart_items %}
                <div style="display: flex; gap: 1.5rem; padding: 1.5rem; background: var(--white); border-radius: 8px; margin-bottom: 1rem; box-shadow: var(--shadow);">
                    <img src="{{ item.image }}" alt="{{ item.name }}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 4px;">
                    <div style="flex: 1;">
                        <h3>{{ item.name }}</h3>
                        <p style="color: var(--secondary);">{{ item.category }}</p>
                        <div style="margin-top: 0.5rem;">
                            <strong>${{ item.price }}</strong>
                        </div>
                    </div>
                    <div style="display: flex; flex-direction: column; justify-content: space-between;">
                        <a href="/cart/remove/{{ item.id }}" class="btn btn-danger" style="padding: 0.5rem 1rem; font-size: 0.875rem;">Remove</a>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <div style="background: var(--white); padding: 2rem; border-radius: 8px; box-shadow: var(--shadow); height: fit-content;">
                <h2 style="margin-bottom: 1.5rem;">Order Summary</h2>
                <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                    <span>Subtotal</span>
                    <span>${{ subtotal }}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                    <span>Shipping</span>
                    <span>Free</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem; font-size: 1.25rem; font-weight: bold;">
                    <span>Total</span>
                    <span>${{ total }}</span>
                </div>
                <a href="/checkout" class="btn btn-primary" style="display: block; text-align: center;">Proceed to Checkout</a>
            </div>
        </div>
    {% else %}
        <div style="text-align: center; padding: 3rem; background: var(--white); border-radius: 8px;">
            <h3>Your cart is empty</h3>
            <p style="color: var(--secondary); margin: 1rem 0;">Add some products to get started!</p>
            <a href="/products" class="btn btn-primary">Browse Products</a>
        </div>
    {% endif %}
</div>
""")

ABOUT_PAGE = BASE_LAYOUT.replace("{% block title %}Galaxy Electronics - Premium Tech Store{% endblock %}", "About Us - Galaxy Electronics").replace("{% block content %}{% endblock %}", """
<div class="container">
    <h1 style="text-align: center; margin-bottom: 3rem;">About Galaxy Electronics</h1>
    
    <div style="max-width: 800px; margin: 0 auto; line-height: 1.8;">
        <p style="font-size: 1.125rem; margin-bottom: 1.5rem;">
            Galaxy Electronics is your premier destination for the latest technology products. Since 2020, we've been committed to providing our customers with cutting-edge electronics at competitive prices.
        </p>
        
        <h2 style="margin-bottom: 1rem;">Our Mission</h2>
        <p style="margin-bottom: 1.5rem;">
            To make technology accessible to everyone while maintaining the highest standards of quality and customer service.
        </p>
        
        <h2 style="margin-bottom: 1rem;">Why Choose Us?</h2>
        <ul style="margin-left: 2rem; margin-bottom: 1.5rem;">
            <li>Wide selection of premium products</li>
            <li>Competitive pricing</li>
            <li>Fast and reliable shipping</li>
            <li>Excellent customer support</li>
            <li>Secure payment options</li>
        </ul>
        
        <h2 style="margin-bottom: 1rem;">Contact Information</h2>
        <p>
            <strong>Email:</strong> support@galaxyelectronics.com<br>
            <strong>Phone:</strong> 1-800-GALAXY<br>
            <strong>Address:</strong> 123 Tech Boulevard, Silicon Valley, CA 94025
        </p>
    </div>
</div>
""")

CONTACT_PAGE = BASE_LAYOUT.replace("{% block title %}Galaxy Electronics - Premium Tech Store{% endblock %}", "Contact Us - Galaxy Electronics").replace("{% block content %}{% endblock %}", """
<div class="container">
    <div style="max-width: 600px; margin: 0 auto;">
        <h1 style="text-align: center; margin-bottom: 2rem;">Contact Us</h1>
        
        {% if message_sent %}
        <div class="alert alert-success">
            <strong>Thank you for your message!</strong><br>
            We have received your inquiry and will get back to you within 24-48 hours. Your submission ID is #{{ submission_id }}.
        </div>
        {% endif %}
        
        <div class="form-container">
            <form action="/contact" method="POST">
                <div class="form-group">
                    <label for="name">Name</label>
                    <input type="text" id="name" name="name" placeholder="Your name" required>
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" placeholder="Your email" required>
                </div>
                <div class="form-group">
                    <label for="subject">Subject</label>
                    <input type="text" id="subject" name="subject" placeholder="Subject" required>
                </div>
                <div class="form-group">
                    <label for="message">Message</label>
                    <textarea id="message" name="message" rows="5" placeholder="Your message" required></textarea>
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%;">Send Message</button>
            </form>
        </div>
        
        <div style="margin-top: 2rem; text-align: center; color: var(--secondary);">
            <p>Or reach us directly:</p>
            <p><strong>Email:</strong> support@galaxyelectronics.com</p>
            <p><strong>Phone:</strong> 1-800-GALAXY</p>
        </div>
    </div>
</div>
""")

CHECKOUT_PAGE = BASE_LAYOUT.replace("{% block title %}Galaxy Electronics - Premium Tech Store{% endblock %}", "Checkout - Galaxy Electronics").replace("{% block content %}{% endblock %}", """
<div class="container">
    <div style="margin-bottom: 1rem;">
        <a href="/cart" style="color: var(--primary); text-decoration: none;">&larr; Back to Cart</a>
    </div>
    
    <h1 style="margin-bottom: 2rem;">Checkout</h1>
    
    <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem;">
        <div class="form-container" style="max-width: none;">
            <h2 style="margin-bottom: 1.5rem;">Shipping Information</h2>
            <form action="/checkout" method="POST">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div class="form-group">
                        <label for="first_name">First Name</label>
                        <input type="text" id="first_name" name="first_name" required>
                    </div>
                    <div class="form-group">
                        <label for="last_name">Last Name</label>
                        <input type="text" id="last_name" name="last_name" required>
                    </div>
                </div>
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" value="{{ session.get('email', '') }}" required>
                </div>
                <div class="form-group">
                    <label for="address">Address</label>
                    <input type="text" id="address" name="address" required>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
                    <div class="form-group">
                        <label for="city">City</label>
                        <input type="text" id="city" name="city" required>
                    </div>
                    <div class="form-group">
                        <label for="state">State</label>
                        <input type="text" id="state" name="state" required>
                    </div>
                    <div class="form-group">
                        <label for="zip">ZIP Code</label>
                        <input type="text" id="zip" name="zip" required>
                    </div>
                </div>
                
                <h2 style="margin: 2rem 0 1.5rem 0;">Payment Information</h2>
                <div class="form-group">
                    <label for="card_number">Card Number</label>
                    <input type="text" id="card_number" name="card_number" placeholder="1234 5678 9012 3456" required>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div class="form-group">
                        <label for="expiry">Expiry Date</label>
                        <input type="text" id="expiry" name="expiry" placeholder="MM/YY" required>
                    </div>
                    <div class="form-group">
                        <label for="cvv">CVV</label>
                        <input type="text" id="cvv" name="cvv" placeholder="123" required>
                    </div>
                </div>
                
                <button type="submit" class="btn btn-success" style="width: 100%; padding: 1rem; font-size: 1.1rem;">Place Order - ${{ total }}</button>
            </form>
        </div>
        
        <div style="background: var(--white); padding: 2rem; border-radius: 8px; box-shadow: var(--shadow); height: fit-content;">
            <h2 style="margin-bottom: 1.5rem;">Order Summary</h2>
            {% for item in cart_items %}
            <div style="display: flex; justify-content: space-between; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #e2e8f0;">
                <span>{{ item.name }}</span>
                <span>${{ item.price }}</span>
            </div>
            {% endfor %}
            <div style="display: flex; justify-content: space-between; margin-bottom: 1rem; margin-top: 1rem;">
                <span>Subtotal</span>
                <span>${{ subtotal }}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                <span>Shipping</span>
                <span>Free</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem; font-size: 1.25rem; font-weight: bold;">
                <span>Total</span>
                <span>${{ total }}</span>
            </div>
        </div>
    </div>
</div>
""")

# ==========================================
# 5. ROUTES
# ==========================================

@app.route('/')
def index():
    return render_template_string(HOME_PAGE, products=PRODUCTS)

@app.route('/products')
def products():
    category = request.args.get('category')
    if category:
        filtered = [p for p in PRODUCTS if p['category'] == category]
    else:
        filtered = PRODUCTS
    return render_template_string(PRODUCTS_PAGE, products=filtered, categories=CATEGORIES, category=category)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        return render_template_string(PRODUCT_DETAIL_PAGE, product=product)
    return "Product not found", 404

@app.route('/search')
def search():
    query = request.args.get('q', '')
    # VULNERABILITY: Reflected XSS
    if query:
        results = [p for p in PRODUCTS if query.lower() in p['name'].lower() or query.lower() in p['description'].lower()]
    else:
        results = []
    return render_template_string(SEARCH_RESULTS_PAGE, query=query, results=results, search_query=query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # VULNERABILITY: SQL Injection (Simulated)
        if "'" in username or "OR" in username.upper() or "--" in username:
            session['logged_in'] = True
            session['username'] = 'Hacker/Admin'
            session['is_admin'] = True
            return redirect(url_for('index'))
        
        # Check if user exists in database
        if username in USERS and USERS[username]['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            session['is_admin'] = USERS[username]['is_admin']
            session['email'] = USERS[username]['email']
            return redirect(url_for('index'))
        else:
            return render_template_string(LOGIN_PAGE, error="Invalid credentials")
    
    return render_template_string(LOGIN_PAGE, error=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # VULNERABILITY: No proper validation
        if password != confirm_password:
            return render_template_string(REGISTER_PAGE, error="Passwords do not match")
        
        # VULNERABILITY: Storing passwords in plain text (simulated)
            # Store the user in the simulated database
            USERS[username] = {
                'password': password,
                'email': email,
                'is_admin': False
            }
        # In a real app, this would be stored in a database
        return render_template_string(REGISTER_PAGE, success="Account created successfully! Please login.")
    
    return render_template_string(REGISTER_PAGE, error=None, success=None)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    username = session.get('username')
    # VULNERABILITY: IDOR potential (simulated order data)
    recent_orders = [
        {'id': 1001, 'date': '2026-03-10', 'total': 1299.99, 'status': 'Delivered'},
        {'id': 1002, 'date': '2026-03-12', 'total': 399.99, 'status': 'Shipped'},
    ]
    
    return render_template_string(
        DASHBOARD_PAGE,
        order_count=len(recent_orders),
        total_spent=1699.98,
        cart_count=len(session.get('cart', [])),
        recent_orders=recent_orders
    )

@app.route('/orders')
def orders():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    username = session.get('username')
    # Get user's orders from simulated database
    user_orders_data = USER_ORDERS.get(username, [])
    
    return render_template_string(ORDERS_PAGE, orders=user_orders_data)

@app.route('/admin')
def admin():
    if not session.get('logged_in') or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    return render_template_string(
        ADMIN_PAGE,
        total_users=25,
        total_orders=len(USER_ORDERS),
        total_contacts=len(CONTACT_SUBMISSIONS),
        total_revenue=45230.50,
        contact_submissions=CONTACT_SUBMISSIONS,
        all_orders=[]
    )

@app.route('/cart')
def cart():
    # VULNERABILITY: Cart data from session (manipulatable)
    cart = session.get('cart', [])
    cart_items = []
    subtotal = 0
    
    for item_id in cart:
        product = next((p for p in PRODUCTS if p['id'] == item_id), None)
        if product:
            cart_items.append(product)
            subtotal += product['price']
    
    return render_template_string(
        CART_PAGE,
        cart_items=cart_items,
        subtotal=subtotal,
        total=subtotal
    )

@app.route('/cart/add/<int:product_id>')
def cart_add(product_id):
    cart = session.get('cart', [])
    cart.append(product_id)
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:product_id>')
def cart_remove(product_id):
    cart = session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    cart = session.get('cart', [])
    cart_items = []
    subtotal = 0
    
    for item_id in cart:
        product = next((p for p in PRODUCTS if p['id'] == item_id), None)
        if product:
            cart_items.append(product)
            subtotal += product['price']
    
    if request.method == 'POST':
        # Create order
        username = session.get('username')
        order_id = len(USER_ORDERS) + 1001
        order = {
            'id': order_id,
            'user': username,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'items': ', '.join([item['name'] for item in cart_items]),
            'total': subtotal,
            'status': 'Processing'
        }
        
        # Add to user's orders
        if username not in USER_ORDERS:
            USER_ORDERS[username] = []
        USER_ORDERS[username].append(order)
        
        # Clear cart
        session['cart'] = []
        
        return redirect(url_for('orders'))
    
    return render_template_string(
        CHECKOUT_PAGE,
        cart_items=cart_items,
        subtotal=subtotal,
        total=subtotal
    )

@app.route('/about')
def about():
    return render_template_string(ABOUT_PAGE)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # VULNERABILITY: No input sanitization
        # Store contact submission
        submission_id = len(CONTACT_SUBMISSIONS) + 1
        submission = {
            'id': submission_id,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'subject': request.form.get('subject'),
            'message': request.form.get('message'),
            'status': 'New'
        }
        CONTACT_SUBMISSIONS.append(submission)
        
        return render_template_string(CONTACT_PAGE, message_sent=True, submission_id=submission_id)
    
    return render_template_string(CONTACT_PAGE, message_sent=False)

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    results = [p for p in PRODUCTS if query.lower() in p['name'].lower()]
    return jsonify(results)

@app.route('/api/reviews', methods=['POST'])
def api_reviews():
    # VULNERABILITY: No authentication required, no sanitization
    data = request.get_json()
    product_id = data.get('product_id')
    review = data.get('review')
    
    # In a real app, this would be stored in database
    # Here we're just simulating the vulnerability
    return jsonify({'status': 'success'})

@app.route('/static/style.css')
def serve_css():
    return CUSTOM_CSS, 200, {'Content-Type': 'text/css'}

@app.route('/static/app.js')
def serve_js():
    return APP_JS_CONTENT, 200, {'Content-Type': 'text/javascript'}

if __name__ == '__main__':
    print("=" * 60)
    print("  GALAXY ELECTRONICS - PUBLIC E-COMMERCE SITE")
    print("  Access at: http://127.0.0.1:5000")
    print("=" * 60)
    print("  USER CREDENTIALS:")
    print("  Username: user")
    print("  Password: user123")
    print("")
    print("  ADMIN CREDENTIALS:")
    print("  Username: admin")
    print("  Password: admin123")
    print("=" * 60)
    print("  Features:")
    print("  - Complete navigation between all pages")
    print("  - Shopping cart with checkout")
    print("  - User dashboard and orders")
    print("  - Admin portal to view contact submissions")
    print("  - Product catalog with categories")
    print("  - Contact form with admin view")
    print("  - Search functionality (XSS vulnerability)")
    print("  - Product reviews (XSS vulnerability)")
    print("  - Login (SQLi vulnerability)")
    print("=" * 60)
    app.run(debug=True, port=5000)
