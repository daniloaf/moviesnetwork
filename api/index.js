const dotenv = require('dotenv');
dotenv.config();

const app = require('./app');

const port = process.env.PORT;

app.use((err, req, res, next) => {
  console.error(err);
  res.status(err.status || 400).send(err);
});

app.listen(port, (err) => {
  if (err) {
    console.error(err);
    console.error('Could not start server');
  } else {
    console.log('App listening on port', port);
  }
});