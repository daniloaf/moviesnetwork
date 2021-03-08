const express = require('express');

const dataController = require('../controllers/data');

const router = express.Router();

router.get('/searchArtist', dataController.searchArtist);


module.exports = router;