// Authentication Module
// Client-side authentication logic

const AUTH_CONFIG = {
    tokenEndpoint: "https://api.galaxy-electronics.com/auth/token",
    refreshEndpoint: "https://api.galaxy-electronics.com/auth/refresh",
    // VULNERABLE: Hardcoded credentials
    clientId: "galaxy_web_client_123",
    clientSecret: "secret_abc123xyz"
};

// VULNERABLE: Token stored in localStorage
function setToken(token) {
    localStorage.setItem('auth_token', token);
    localStorage.setItem('token_expiry', Date.now() + 3600000); // 1 hour
}

function getToken() {
    return localStorage.getItem('auth_token');
}

function isAuthenticated() {
    const token = getToken();
    const expiry = localStorage.getItem('token_expiry');
    return token && expiry && Date.now() < parseInt(expiry);
}

// VULNERABLE: Refresh token logic exposed
function refreshToken() {
    const token = getToken();
    if (!token) return;
    
    fetch(AUTH_CONFIG.refreshEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            token: token,
            client_id: AUTH_CONFIG.clientId,
            client_secret: AUTH_CONFIG.clientSecret
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.token) {
            setToken(data.token);
        }
    })
    .catch(error => {
        console.error('Token refresh failed:', error);
    });
}

// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    if (!isAuthenticated()) {
        // Redirect to login if not authenticated
        if (window.location.pathname !== '/login' && 
            window.location.pathname !== '/register') {
            // Note: In real app, this would redirect
            console.log('User not authenticated');
        }
    } else {
        // Check if token needs refresh
        const expiry = localStorage.getItem('token_expiry');
        if (expiry && Date.now() > parseInt(expiry) - 300000) { // 5 minutes before expiry
            refreshToken();
        }
    }
});
