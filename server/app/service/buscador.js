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

const buscarNumeroTweetsClassificados = (TweetsCandidatoDiaClassificacao, candidatoId, callback) => {
  const query = TweetsCandidatoDiaClassificacao.find({ "candidato_id": candidatoId });
  query.select('date count positivos negativos neutros');
  query.exec((err, tweets) => {
    if (err) {
      console.log('Erro na busca pelos números de tweets diários:', err);
    } else {
      callback(tweets);
    }
  });
};

module.exports = {
  buscarNumeroTweets: buscarNumeroTweets,
  buscarNumeroTweetsClassificados: buscarNumeroTweetsClassificados
};
