const mongoose = require('mongoose');
const schema = mongoose.Schema;

module.exports = () => {
  const classificacaoSchema = schema({
    candidato_id: Number,
    candidato: String,
    date: String,
    count: Number,
    positivos: Number,
    negativos: Number,
    neutros: Number
  });

  return mongoose.model('TweetCandidatoDiaClassificacao', classificacaoSchema, 'tweets_candidato_dia_classificacao');
};
