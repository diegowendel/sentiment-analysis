module.exports = (app) => {
  const {tweet} = app.controllers;
  app.get('/api/tweets', tweet.main);
  app.get('/api/tweets/quantidade/:candidato', tweet.countTweets);
};
