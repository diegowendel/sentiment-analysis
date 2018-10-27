const buscarNumeroTweets = (TweetsCandidatoDia, candidatoId, callback) => {
  const query = TweetsCandidatoDia.find({ "candidato_id": candidatoId });
  query.select('date count');
  query.exec((err, tweets) => {
    if (err) {
      console.log('Erro na busca pelos números de tweets diários:', err);
    } else {
      callback(tweets);
    }
  });
};

module.exports = {
  buscarNumeroTweets: buscarNumeroTweets
};
