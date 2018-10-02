module.exports = (app) => {
  const HomeController = {
    home(req, res) {
      res.render('home');
    }
  };
  return HomeController;
};
