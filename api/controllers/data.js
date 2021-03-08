const _ = require('lodash');
const fetch =  require('node-fetch');

const imdbApiBaseUrl = process.env.IMDB_API_BASE_URL;
const imbdApiKey = process.env.IMDB_API_KEY;

const searchArtist = async (req, res, next) => {
  try {
    const { name } = req.query;
    console.log(`${imdbApiBaseUrl}/${imbdApiKey}/searchName/${name}`);
    const response = await fetch(`${imdbApiBaseUrl}/SearchName/${imbdApiKey}/${name}`);
    const responseData = await response.json();

    const { results, errorMessage } = responseData;

    if (!_.isEmpty(errorMessage)) {
      throw 'The search result an error';
    }

    const artists = results.map(result => ({
      id: result.id, name: result.title, image: result.image, description: result.description
    }));

    res.json(artists);
  } catch (err) {
    next(err);
  }
};

module.exports = {
  searchArtist
};