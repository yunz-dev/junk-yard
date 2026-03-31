const API_BASE = '/api';

export const flashcardAPI = {
  getAll: async (category = null, studied = null) => {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (studied !== null) params.append('studied', studied);
    const query = params.toString();
    const response = await fetch(`${API_BASE}/flashcards${query ? '?' + query : ''}`);
    return response.json();
  },

  create: async (flashcard) => {
    const response = await fetch(`${API_BASE}/flashcards`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(flashcard),
    });
    return response.json();
  },

  update: async (id, updates) => {
    const response = await fetch(`${API_BASE}/flashcards/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates),
    });
    return response.json();
  },

  delete: async (id) => {
    const response = await fetch(`${API_BASE}/flashcards/${id}`, {
      method: 'DELETE',
    });
    return response.json();
  },

  getCategories: async () => {
    const response = await fetch(`${API_BASE}/categories`);
    return response.json();
  },

  resetStudied: async () => {
    const response = await fetch(`${API_BASE}/reset`, {
      method: 'POST',
    });
    return response.json();
  },
};
