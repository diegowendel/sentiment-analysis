const mongoose = require('mongoose');
const schema = mongoose.Schema;

module.exports = () => {
  const tweetSchema = schema({
    retweeted: Boolean,
    is_quote_status: Boolean,
    lang: String,
    text: String,
    in_reply_to_screen_name: String,
    created_at: Date
  });

  return mongoose.model('Tweet', tweetSchema, 'tweets');
};
