const _ = require('lodash');
const fetch =  require('node-fetch');

const imdbApiBaseUrl = process.env.IMDB_API_BASE_URL;
const imbdApiKey = process.env.IMDB_API_KEY;

const MIN_SEARCH_LENGTH = 3;
const ACCEPTED_ROLES = [ "Actor", "Actress" ];

const searchArtist = async (req, res, next) => {
  try {
    const { name } = req.query;

    if (name?.length < MIN_SEARCH_LENGTH) {
      return res.json([]);
    }

    const response = await fetch(`${imdbApiBaseUrl}/SearchName/${imbdApiKey}/${name}`);
    const responseData = await response.json();

    const { results, errorMessage } = responseData;

    if (!_.isEmpty(errorMessage)) {
      console.log(errorMessage)
      throw 'The search result an error';
    }
    
    const artists = results.map(result => ({
      id: result.id, name: result.title, image: result.image, description: result.description
    }));

    res.json(artists);
  } catch (err) {
    console.log(err)
    next(err);
  }
};

const getArtistMovies = async (req, res, next) => {
  try {
    const { artistId } = req.params;
    const response = await fetch(`${imdbApiBaseUrl}/Name/${imbdApiKey}/${artistId}`);
    const responseData = await response.json();

    const movies = responseData
      .castMovies
      .filter(m => _.includes(ACCEPTED_ROLES, m.role))
      .map(m => ({ id: m.id, title: m.title, image: m.image, artistRole: m.role, artistId: artistId }));

    res.json(movies);
  } catch (err) {
    console.log(err)
    next(err);
  }
}

module.exports = {
  searchArtist,
  getArtistMovies
};