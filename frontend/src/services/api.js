import axios from 'axios';

// Auto-detect environment
const isDevelopment = import.meta.env.DEV;

// Production URL from environment variable, fallback to localhost in dev
const API_BASE = isDevelopment
    ? 'http://localhost:5001/api'
    : (import.meta.env.VITE_API_URL || 'https://email-productivity-agent-z0qd.onrender.com/api');

console.log('🌐 API Base URL:', API_BASE);

const api = axios.create({
    baseURL: API_BASE,
    headers: {
        'Content-Type': 'application/json'
    },
    timeout: 60000  // 60 second timeout for AI processing
});

// Add response interceptor for better error handling
api.interceptors.response.use(
    response => response,
    error => {
        console.error('API Error:', error);
        if (error.code === 'ECONNABORTED') {
            console.error('Request timeout - backend may be processing');
        }
        return Promise.reject(error);
    }
);

// NEW: Load mock email data
export const loadMockEmails = () => {
    return api.post('/emails/load-mock');
};

// Fetch real emails from Gmail
export const fetchEmails = (maxResults = 20) => {
    return api.get(`/emails/fetch?max_results=${maxResults}`);
};

// Process emails with AI
export const processEmails = () => {
    return api.post('/emails/process');
};

// Get stored emails
export const getEmails = () => {
    return api.get('/emails');
};

// Chat with email agent
export const chatWithAgent = (email, query, history) => {
    return api.post('/chat', { email, query, history });
};

// Generate draft reply
export const generateDraft = (email) => {
    return api.post('/draft/generate', { email });
};

// Get all drafts
export const getDrafts = () => {
    return api.get('/drafts');
};

// Delete a draft
export const deleteDraft = (draftId) => {
    return api.delete(`/drafts/${draftId}`);
};

// Get prompt configurations
export const getPrompts = () => {
    return api.get('/prompts');
};

// Update prompt configurations
export const updatePrompts = (prompts) => {
    return api.put('/prompts', prompts);
};

export default api;