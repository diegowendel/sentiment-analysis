const buscador = require('../service/buscador');
const objectUtils = require('../utils/objectUtils');
const moment = require('moment');

module.exports = (app) => {
  const Tweets = app.models.tweet;

  const TweetController = {
    main(req, res) {
      const query = Tweets.find({"text": /lula/i});
      query.select('text');
      query.exec((err, status) => {
        if (err) {
          res.status(500).send(err);
        } else {
          res.status(200).json(status);
        }
      });
    },
    countTweets(req, res) {
      const candidato = Number(req.params.candidato);
      buscador.buscarMes(Tweets, candidato, function(aggregateResult) {
        if (aggregateResult) {
          let dataToChart = aggregateResult.map(function(obj) {
            return Object.keys(obj).sort().map(function(key) {
              if (objectUtils.isObject(obj[key])) {
                return moment(obj[key].date, 'DD-MM-YYYY').toDate().valueOf();
              }
              return obj[key];
            });
          });
          res.status(200).json(dataToChart);
        } else {
          res.status(500).send('');
        }
      });
    }
  };
  
  return TweetController;
};
