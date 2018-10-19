const obterQueryString = (candidato) => {
  switch(candidato) {
    case 1:
      return "alvaro";
    case 2:
      return "daciolo";
    case 3:
      return "ciro";
    case 4:
      return "haddad";
    case 5:
      return "alckmin";
    case 6:
      return "boulos";
    case 7:
      return "meirelles";
    case 8:
      return "bolsonaro";
    case 9:
      return "amoedo";
    case 10:
      return "goulart";
    case 11:
      return "eymael";
    case 12:
      return "marina";
    case 13:
      return "vera";
    case 14:
      return "lula";
    default:
      return "lula";
  }
}

const buscarMes = (Tweets, candidato, callback) => {
  const queryString = obterQueryString(candidato);
  Tweets.aggregate([
    {
      $match : {
        $and: [
          {
            $and : [
              {
                "timestamp_ms" : {
                  $gte : Date.UTC(2018, 9, 1, 0, 0, 0).toString()
                }
              },
              {
                "timestamp_ms" : {
                  $lte : Date.UTC(2018, 9, 31, 0, 0, 0).toString()
                }
              }
            ]
          },
          {
            "text": {
              $regex: queryString,
              $options: 'i'
            }
          }
        ]
      }
    },
    {
      $project: {
        "date": {
          $dateToString: {
            "format": "%d-%m-%Y",
            "date": {
              $toDate: {
                $toLong: "$timestamp_ms"
              }
            }
          }
        }
      }
    },
    {
      $group: {
        _id: {
          "lang": "$lang",
          "date": "$date"
        },
        count: {$sum: 1}
      }
    },
    {
      $sort: {
        "_id.date": 1.0
      }
    }
  ], function (err, result) {
    if (err) {
      console.log('Erro no aggregate:', err);
    } else {
      callback(result);
    }
  });
};

module.exports = {
  buscarMes: buscarMes
};
