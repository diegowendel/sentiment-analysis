const app = require('./config/express')();
const config = require('./config/config')();
const fs = require('fs');
const https = require('https');
const logger = require('./app/utils/logger');
require('./config/database')(config.MONGODB_URI);

// Initialize the app
https.createServer({
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.cert')
}, app).listen(config.PORT, () => {
  logger.success('Sentiment Analysis Server Running on Port ' + config.PORT);
});
