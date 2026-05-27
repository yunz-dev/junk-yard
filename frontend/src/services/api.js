const API_BASE = '/api';

const getToken = () => localStorage.getItem('token');

const authHeaders = () => {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const authAPI = {
  login: async (username, password) => {
    const response = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Login failed');
    return data;
  },

  register: async (username, password) => {
    const response = await fetch(`${API_BASE}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Registration failed');
    return data;
  },
};

export const flashcardAPI = {
  getAll: async (category = null, studied = null) => {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (studied !== null) params.append('studied', studied);
    const query = params.toString();
    const response = await fetch(`${API_BASE}/flashcards${query ? '?' + query : ''}`, {
      headers: authHeaders(),
    });
    return response.json();
  },

  create: async (flashcard) => {
    const response = await fetch(`${API_BASE}/flashcards`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...authHeaders() },
      body: JSON.stringify(flashcard),
    });
    return response.json();
  },

  update: async (id, updates) => {
    const response = await fetch(`${API_BASE}/flashcards/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', ...authHeaders() },
      body: JSON.stringify(updates),
    });
    return response.json();
  },

  delete: async (id) => {
    const response = await fetch(`${API_BASE}/flashcards/${id}`, {
      method: 'DELETE',
      headers: authHeaders(),
    });
    return response.json();
  },

  getCategories: async () => {
    const response = await fetch(`${API_BASE}/categories`, {
      headers: authHeaders(),
    });
    return response.json();
  },

  recordView: async (id) => {
    try {
      await fetch(`${API_BASE}/flashcards/${id}/view`, {
        method: 'POST',
        headers: authHeaders(),
      });
    } catch (_) {
      // ignore
    }
  },

  markStudied: async (id, studied = true) => {
    const response = await fetch(`${API_BASE}/flashcards/${id}/studied`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', ...authHeaders() },
      body: JSON.stringify({ studied }),
    });
    return response.json();
  },
};

export const userAPI = {
  getMe: async () => {
    const response = await fetch(`${API_BASE}/me`, {
      headers: authHeaders(),
    });
    return response.json();
  },

  getAll: async () => {
    const response = await fetch(`${API_BASE}/users`, {
      headers: authHeaders(),
    });
    return response.json();
  },

  getOne: async (id) => {
    const response = await fetch(`${API_BASE}/users/${id}`, {
      headers: authHeaders(),
    });
    return response.json();
  },

  update: async (id, data) => {
    const response = await fetch(`${API_BASE}/users/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', ...authHeaders() },
      body: JSON.stringify(data),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || 'Update failed');
    return result;
  },

  delete: async (id) => {
    const response = await fetch(`${API_BASE}/users/${id}`, {
      method: 'DELETE',
      headers: authHeaders(),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || 'Delete failed');
    return result;
  },

  changePassword: async (current_password, new_password) => {
    const response = await fetch(`${API_BASE}/me`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', ...authHeaders() },
      body: JSON.stringify({ current_password, new_password }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || 'Password change failed');
    return result;
  },

  resetProgress: async (userId) => {
    const response = await fetch(`${API_BASE}/users/${userId}/reset-progress`, {
      method: 'POST',
      headers: authHeaders(),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || 'Reset failed');
    return result;
  },
};
