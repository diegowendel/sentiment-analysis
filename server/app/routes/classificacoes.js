module.exports = (app) => {
  const {classificacoes} = app.controllers;
  app.get('/classificacoes', classificacoes.main);
  app.get('/api/classificacoes/quantidade/:candidato', classificacoes.countClassificacoes);
};
