const express = require('express');

const dataController = require('../controllers/data');

const router = express.Router();

router.get('/searchArtist', dataController.searchArtist);
router.get('/artists/:artistId/movies', dataController.getArtistMovies);

module.exports = router;