$(document).ready(function() {

  console.log(progLangData);

  data = {
      datasets: [{
          data: [10, 20, 30]
      }],

      // These labels appear in the legend and in the tooltips when hovering different arcs
      labels: [
          moopData,
          'Yellow',
          'Blue'
      ],
      backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)'
      ],
      borderColor: [
                 'rgba(255,99,132,1)',
                 'rgba(54, 162, 235, 1)',
                 'rgba(255, 206, 86, 1)'
     ]
  };


  var ctx = document.getElementById("myChart");
  var myDoughnutChart = new Chart(ctx, {
    type: 'doughnut',
    data: data,
    options: {}
  });

});
