const buscador = require('../service/buscador');

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
          res.status(200).json(aggregateResult);
        } else {
          res.status(500).send('');
        }
      });
    }
  };
  
  return TweetController;
};
