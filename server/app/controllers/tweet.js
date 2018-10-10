module.exports = (app) => {
  const Tweets = app.models.tweet;

  const TweetController = {
    main(req, res) {
      const query = Tweets.find({"text": "lula"}).limit(5);
      query.select('text');
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
