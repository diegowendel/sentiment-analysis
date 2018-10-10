$.getJSON(
  'https://cdn.rawgit.com/highcharts/highcharts/057b672172ccc6c08fe7dbb27fc17ebca3f5b770/samples/data/usdeur.json',
  function (data) {
      Highcharts.chart('container', {
          chart: {
              zoomType: 'x'
          },
          title: {
              text: 'Número de tweets ao longo do tempo'
          },
          subtitle: {
              text: document.ontouchstart === undefined ?
                'Clique e arraste em uma área do gráfico para aumentar o zoom' : 'Pinch the chart to zoom in'
          },
          xAxis: {
              type: 'datetime'
          },
          yAxis: {
              title: {
                  text: 'Número de tweets'
              }
          },
          legend: {
              enabled: false
          },
          plotOptions: {
              area: {
                  fillColor: {
                      linearGradient: {
                          x1: 0,
                          y1: 0,
                          x2: 0,
                          y2: 1
                      },
                      stops: [
                          [0, Highcharts.getOptions().colors[0]],
                          [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                      ]
                  },
                  marker: {
                      radius: 2
                  },
                  lineWidth: 1,
                  states: {
                      hover: {
                          lineWidth: 1
                      }
                  },
                  threshold: null
              }
          },

          series: [{
              type: 'area',
              name: 'Quantidade de tweets',
              data: data
          }]
      });
  }
);
