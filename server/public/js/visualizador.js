$('select').on('change', function(e){
  console.log(this.value, this.options[this.selectedIndex].value, $(this).find("option:selected").val(),);
  $.ajax({
    url: `/api/tweets/quantidade/` + this.value,
    type: 'GET',
    dataType: 'json',
    success: (jsonData) => {
      console.log(jsonData);
    },
    error: () => {
      console.log('FAILED');
    },
  });
});
