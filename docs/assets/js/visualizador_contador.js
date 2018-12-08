const chartOptions = {
  chart: {
    renderTo: 'container',
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
    id: 'tweets',
    type: 'area',
    name: 'Quantidade de tweets',
    data: []
  }]
};

let chart = new Highcharts.Chart(chartOptions);

$('select').on('change', function(e) {
  const opcao = this.value;
  const nomeCandidato = $(this).find("option:selected").text();

  if (opcao == 0) {
    $('#nome_candidato').text(null);
  } else {
    $('#nome_candidato').text(nomeCandidato);
  }

  $.ajax({
    url: `http://54.94.247.69/api/tweets/quantidade/` + this.value,
    type: 'GET',
    dataType: 'json',
    success: (jsonData) => {
      chart.destroy();
      chartOptions.series[0].data = jsonData;
      chart = new Highcharts.Chart(chartOptions);
    },
    error: () => {
      console.log('Erro no AJAX da API de tweets');
    },
  });
});
