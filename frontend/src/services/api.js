import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const searchMovies = async (query) => {
  try {
    const response = await axios.get(`${API_URL}/search`, {
      params: { query }
    });
    return response.data;
  } catch (error) {
    console.error('Error searching movies:', error);
    throw error;
  }
}; 