const _ = require('lodash');
const fetch =  require('node-fetch');

const imdbApiBaseUrl = process.env.IMDB_API_BASE_URL;
const imbdApiKey = process.env.IMDB_API_KEY;

const MIN_SEARCH_LENGTH = 3;

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

    // const results = [{"id":"nm0187719","name":"Terry Crews","image":"https://imdb-api.com/images/original/MV5BMjE1ODY0NzE4N15BMl5BanBnXkFtZTcwMTY5Mzk0Mw@@._V1_Ratio0.7273_AL_.jpg","description":"(I) (Actor, Idiocracy (2006))"},{"id":"nm7305197","name":"Terry Crews","image":"https://imdb-api.com/images/original/nopicture.jpg","description":"(III)"},{"id":"nm1131702","name":"Terry Crews","image":"https://imdb-api.com/images/original/nopicture.jpg","description":"(II) (Additional Crew, Chuck & Buck (2000))"},{"id":"nm0187705","name":"Jerry Crews","image":"https://imdb-api.com/images/original/nopicture.jpg","description":"(Actor, The Waltons (1972))"},{"id":"nm9445903","name":"Terry Crew","image":"https://imdb-api.com/images/original/nopicture.jpg","description":""},{"id":"nm0187704","name":"Harry Crews","image":"https://imdb-api.com/images/original/nopicture.jpg","description":"(Additional Crew, Charming Billy (1999))"},{"id":"nm12364141","name":"Jerry Crew","image":"https://imdb-api.com/images/original/MV5BZTk4NTE0NjQtYTM2ZS00N2JiLWE2YjQtNjQ3MzFmOWY2MzY3XkEyXkFqcGdeQXVyNjUxMjc1OTM@._V1_Ratio0.7273_AL_.jpg","description":""},{"id":"nm6046042","name":"Terry Cress","image":"https://imdb-api.com/images/original/nopicture.jpg","description":"(Self, Canada's Worst Handyman (2006))"},{"id":"nm12068314","name":"Terry Creasey","image":"https://imdb-api.com/images/original/nopicture.jpg","description":"(Self, Bobby (2016))"},{"id":"nm8581450","name":"Terry Creasy","image":"https://imdb-api.com/images/original/nopicture.jpg","description":"(Actor, Cosy Cool (1977))"}]

    const artists = results.map(result => ({
      id: result.id, name: result.name, image: result.image, description: result.description
    }));

    res.json(artists);
  } catch (err) {
    console.log(err)
    next(err);
  }
};

module.exports = {
  searchArtist
};