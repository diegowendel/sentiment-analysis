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
      let queryString;
      switch(candidato) {
        case 1:
          queryString = "alvaro";
          break;
        case 2:
          queryString = "daciolo";
          break;
        case 3:
          queryString = "ciro";
          break;
        case 4:
          queryString = "haddad";
          break;
        case 5:
          queryString = "alckmin";
          break;
        case 6:
          queryString = "boulos";
          break;
        case 7:
          queryString = "meirelles";
          break;
        case 8:
          queryString = "bolsonaro";
          break;
        case 9:
          queryString = "amoedo";
          break;
        case 10:
          queryString = "goulart";
          break;
        case 11:
          queryString = "eymael";
          break;
        case 12:
          queryString = "marina";
          break;
        case 13:
          queryString = "vera";
          break;
        case 14:
          queryString = "lula";
          break;
        default:
          queryString = "lula";
      }
      const query = Tweets.find({"text": { $regex: queryString, $options: 'i' }});
      query.select('text created_at');
      query.exec((err, status) => {
        if (err) {
          res.status(500).send(err);
        } else {
          res.status(200).json(status);
        }
      });
    }
  };
  
  return TweetController;
};
