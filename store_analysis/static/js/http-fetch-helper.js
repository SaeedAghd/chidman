/**
 * HTTP Fetch Helper for Development Server
 * Fixes SSL protocol errors by ensuring HTTP is used instead of HTTPS
 */

function getHttpUrl(url) {
    // Ensure we use HTTP for development server
    if (url.startsWith('https://127.0.0.1:8000')) {
        return url.replace('https://127.0.0.1:8000', 'http://127.0.0.1:8000');
    } else if (url.startsWith('https://localhost:8000')) {
        return url.replace('https://localhost:8000', 'http://localhost:8000');
    } else if (url.startsWith('https://')) {
        // For any other HTTPS URL, try to convert to HTTP for development
        return url.replace('https://', 'http://');
    }
    return url;
}

function httpFetch(url, options = {}) {
    const httpUrl = getHttpUrl(url);
    console.log('Fetching:', httpUrl);
    return fetch(httpUrl, options);
}

// Make functions globally available
window.getHttpUrl = getHttpUrl;
window.httpFetch = httpFetch;
