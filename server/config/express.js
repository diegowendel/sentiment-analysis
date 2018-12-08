const bodyParser = require('body-parser');
const express = require('express');
const load = require('express-load');

module.exports = () => {
  // Express app
  const app = express();

  // Support parsing of application/json type post data
  app.use(bodyParser.json());
  // Support parsing of application/x-www-form-urlencoded post data
  app.use(bodyParser.urlencoded({extended: true}));
  // Tell express that public is the root of our public web folder
  app.use(express.static('./public'));
  // CORS
  app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
  });

  app.set('view engine', 'ejs');
  app.set('views', './app/views');

  load('models', {cwd: 'app'})
    .then('controllers')
    .then('routes')
    .into(app);

  return app;
};
