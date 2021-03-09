import api from './axios';

export const searchArtist = async (searchTerm) => {
  const response = await api.get('/data/searchArtist', { data: { searchTerm } });
  return response.data;
};