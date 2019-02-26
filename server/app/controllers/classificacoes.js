const buscador = require('../service/buscador');
const moment = require('moment');

module.exports = (app) => {
  const TweetCandidatoDiaClassificacao = app.models.tweetCandidatoDiaClassificacao;

  const ClassificacoesController = {
    main(req, res) {
      res.render('classificacao');
    },
    countClassificacoes(req, res) {
      const candidato = Number(req.params.candidato);
      buscador.buscarNumeroTweetsClassificados(TweetCandidatoDiaClassificacao, candidato, function(queryResult) {
        if (queryResult) {
          let dadosPositivos = queryResult.map(function(obj) {
            return [moment(obj.date, 'DD-MM-YYYY').toDate().valueOf(), obj.positivos];
          });
          dadosPositivos = dadosPositivos.sort(function Comparator(a, b) {
            if (a[0] < b[0]) return -1;
            if (a[0] > b[0]) return 1;
            return 0;
          });

          let dadosNegativos = queryResult.map(function(obj) {
            return [moment(obj.date, 'DD-MM-YYYY').toDate().valueOf(), obj.negativos*(-1)];
          });
          dadosNegativos = dadosNegativos.sort(function Comparator(a, b) {
            if (a[0] < b[0]) return -1;
            if (a[0] > b[0]) return 1;
            return 0;
          });

          let dadosNeutros = queryResult.map(function(obj) {
            return [moment(obj.date, 'DD-MM-YYYY').toDate().valueOf(), obj.neutros];
          });
          dadosNeutros = dadosNeutros.sort(function Comparator(a, b) {
            if (a[0] < b[0]) return -1;
            if (a[0] > b[0]) return 1;
            return 0;
          });

          let dados = {
            "positivos": dadosPositivos,
            "negativos": dadosNegativos,
            "neutros": dadosNeutros
          }

          res.status(200).json(dados);
        } else {
          res.status(500).send('');
        }
      });
    }
  };

  return ClassificacoesController;
};
