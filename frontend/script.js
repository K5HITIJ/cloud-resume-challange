// Visitor counter functionality
document.addEventListener('DOMContentLoaded', function() {
    const visitorCountElement = document.getElementById('visitor-count');
    
    // API Gateway endpoint URL - Updated with actual endpoint
    const API_ENDPOINT = 'https://gyi4noddk5.execute-api.us-east-1.amazonaws.com/Prod/visitor-count';
    
    async function updateVisitorCount() {
        try {
            visitorCountElement.classList.add('loading');
            
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'increment'
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Display the visitor count
            visitorCountElement.textContent = data.count || data.visitor_count || 'Error';
            visitorCountElement.classList.remove('loading');
            
        } catch (error) {
            console.error('Error fetching visitor count:', error);
            visitorCountElement.textContent = 'Error loading count';
            visitorCountElement.classList.remove('loading');
            visitorCountElement.classList.add('error');
        }
    }
    
    // Get visitor count without incrementing (for page refreshes)
    async function getVisitorCount() {
        try {
            visitorCountElement.classList.add('loading');
            
            const response = await fetch(API_ENDPOINT, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Display the visitor count
            visitorCountElement.textContent = data.count || data.visitor_count || 'Error';
            visitorCountElement.classList.remove('loading');
            
        } catch (error) {
            console.error('Error fetching visitor count:', error);
            // If GET fails, try incrementing (first-time visitor)
            updateVisitorCount();
        }
    }
    
    // Check if this is a new session
    const hasVisited = sessionStorage.getItem('hasVisited');
    
    if (!hasVisited) {
        // New session - increment counter
        updateVisitorCount();
        sessionStorage.setItem('hasVisited', 'true');
    } else {
        // Returning in same session - just get current count
        getVisitorCount();
    }
});

// For local testing - replace with actual API endpoint
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log('Local development mode - visitor counter will not work until deployed');
    document.getElementById('visitor-count').textContent = '42 (Local)';
}
