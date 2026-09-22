/**
 * AI Book Writer v3.0 — Centralized API Client
 * Clean abstraction handling v1 endpoints, error resilience, and event streaming.
 */

class ApiClient {
    constructor(baseUrl = '') {
        this.baseUrl = baseUrl;
    }

    async _request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...(options.headers || {})
        };

        const config = {
            ...options,
            headers
        };

        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                let errorDetail = `HTTP ${response.status} ${response.statusText}`;
                try {
                    const text = await response.text();
                    try {
                        const parsed = JSON.parse(text);
                        errorDetail = parsed.detail || parsed.error || errorDetail;
                    } catch {
                        errorDetail = text.length > 200 ? text.substring(0, 200) + '...' : text;
                    }
                } catch {}
                throw new Error(errorDetail);
            }

            // If empty response or 204
            if (response.status === 204) return null;
            return await response.json();
        } catch (err) {
            console.error(`API request failed [${options.method || 'GET'} ${endpoint}]:`, err);
            throw err;
        }
    }

    async parseSyllabus(text, apiKey = null) {
        return this._request('/api/v1/books/parse-syllabus', {
            method: 'POST',
            body: JSON.stringify({ text, api_key: apiKey })
        });
    }

    async estimateBook(bookData) {
        return this._request('/api/v1/books/estimate', {
            method: 'POST',
            body: JSON.stringify(bookData)
        });
    }

    async createBook(bookData) {
        return this._request('/api/v1/books', {
            method: 'POST',
            body: JSON.stringify(bookData)
        });
    }

    async getBook(bookId) {
        return this._request(`/api/v1/books/${bookId}`);
    }

    async createJob(bookId, apiKey = null) {
        return this._request('/api/v1/jobs', {
            method: 'POST',
            body: JSON.stringify({ book_id: bookId, api_key: apiKey })
        });
    }

    async getJob(jobId) {
        return this._request(`/api/v1/jobs/${jobId}`);
    }

    async cancelJob(jobId) {
        return this._request(`/api/v1/jobs/${jobId}/cancel`, {
            method: 'POST'
        });
    }

    async retryJob(jobId, apiKey = null) {
        return this._request(`/api/v1/jobs/${jobId}/retry`, {
            method: 'POST',
            body: JSON.stringify({ book_id: '', api_key: apiKey })
        });
    }

    async getEvents(jobId, after = null) {
        const query = after ? `?after=${encodeURIComponent(after)}` : '';
        return this._request(`/api/v1/jobs/${jobId}/events${query}`);
    }

    getStreamUrl(jobId) {
        return `/api/v1/jobs/${jobId}/stream`;
    }

    getDownloadUrl(filename) {
        return `/api/v1/files/${encodeURIComponent(filename)}`;
    }
}

const api = new ApiClient();
