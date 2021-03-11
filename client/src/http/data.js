import api from './axios';

export const searchArtist = async (searchTerm) => {
  const response = await api.get('/data/searchArtist', { params: { name: searchTerm }});
  return response.data;
};

export const getArtistMovies = async (artistId) => {
  const response = await api.get(`/data/artists/${artistId}/movies`);
  return response.data;
};