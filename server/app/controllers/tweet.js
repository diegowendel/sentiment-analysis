const buscador = require('../service/buscador');
const moment = require('moment');

module.exports = (app) => {
  const TweetsCandidatoDia = app.models.tweetCandidatoDia;

  const TweetController = {
    countTweets(req, res) {
      const candidato = Number(req.params.candidato);
      buscador.buscarNumeroTweets(TweetsCandidatoDia, candidato, function(queryResult) {
        if (queryResult) {
          let dataToChart = queryResult.map(function(obj) {
            return [moment(obj.date, 'DD-MM-YYYY').toDate().valueOf(), obj.count];
          });

          dataToChart = dataToChart.sort(function Comparator(a, b) {
            if (a[0] < b[0]) return -1;
            if (a[0] > b[0]) return 1;
            return 0;
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
