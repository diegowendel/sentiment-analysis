const mongoose = require('mongoose');
const schema = mongoose.Schema;

module.exports = () => {
  const tweetSchema = schema({
    candidato_id: Number,
    candidato: String,
    date: String,
    count: Number
  });

  return mongoose.model('TweetCandidatoDia', tweetSchema, 'tweets_candidato_dia');
};
