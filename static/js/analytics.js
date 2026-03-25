// Galaxy Electronics Analytics
// configuration 
const ANALYTICS_CONFIG = {
    trackingId: "GA-123456789-1",
    apiEndpoint: "https://analytics.galaxy-electronics.com/v1/track",
    userId: sessionStorage.getItem('user_id') || 'anonymous',
    debug: true
};

// data collection
function trackPageView(page) {
    const data = {
        trackingId: ANALYTICS_CONFIG.trackingId,
        userId: ANALYTICS_CONFIG.userId,
        page: page,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        // : Collecting potentially  data
        referrer: document.referrer,
        cookies: document.cookie
    };
    
    // Send to analytics endpoint
    fetch(ANALYTICS_CONFIG.apiEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Tracking-Key': 'tracking_key_12345' // key
        },
        body: JSON.stringify(data)
    }).catch(error => {
        console.log('Analytics tracking failed:', error);
    });
}

// Track user interactions
function trackEvent(event, data) {
    const eventData = {
        event: event,
        data: data,
        userId: ANALYTICS_CONFIG.userId,
        timestamp: new Date().toISOString()
    };
    
    console.log('Event tracked:', eventData);
}

// Initialize tracking
document.addEventListener('DOMContentLoaded', () => {
    trackPageView(window.location.pathname);
    
    // Track clicks
    document.addEventListener('click', (e) => {
        if (e.target.closest('a') || e.target.closest('button')) {
            trackEvent('click', {
                element: e.target.tagName,
                text: e.target.textContent
            });
        }
    });
});
