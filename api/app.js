const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const router = require('./routes');

const app = express();

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.use(router);

app.use((err, req, res, next) => {
  next({
    status: err.status || 400,
    message: err.message || 'Unexpected error'
  });
});

module.exports = app;