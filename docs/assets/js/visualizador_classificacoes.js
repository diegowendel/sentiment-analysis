const chartOptions = {
  chart: {
    renderTo: 'container',
    type: 'area'
  },
  title: {
    text: 'Classificações de tweets ao longo do tempo'
  },
  xAxis: {
    type: 'datetime'
  },
  yAxis: {
    title: {
      text: 'Número de tweets classificados'
    }
  },
  credits: {
    enabled: false
  },
  series: [
    {
      name: 'Neutros',
      data: [],
      color: '#c1c1d7'
    },
    {
      name: 'Positivos',
      data: [],
      color: '#25488e'
    },
    {
      name: 'Negativos',
      data: [],
      color: '#cc0000'
    }
  ]
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
    url: `/api/classificacoes/quantidade/` + this.value,
    type: 'GET',
    dataType: 'json',
    success: (jsonData) => {
      chart.destroy();
      chartOptions.series[0].data = jsonData.neutros;
      chartOptions.series[1].data = jsonData.positivos;
      chartOptions.series[2].data = jsonData.negativos;
      chart = new Highcharts.Chart(chartOptions);
    },
    error: () => {
      console.log('Erro no AJAX da API de tweets');
    },
  });
});
