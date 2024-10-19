// var ctx = document.getElementById('myChart').getContext('2d');
// var myChart;

// function createChart(tasks, progress, colors) {
//   if (myChart) {
//     myChart.destroy(); // Удаляем старый график
//   }
//   myChart = new Chart(ctx, {
//     type: 'bar',
//     data: {
//       labels: tasks,
//       datasets: [
//         {
//           backgroundColor: colors,
//           data: progress,
//         },
//       ],
//     },
//     options: {
//       legend: { display: false },
//       title: {
//         display: true,
//         text: 'TASK PROGRESS %',
//       },
//     },
//   });
// }

// function updateData() {
//   fetch('/data/')
//     .then((response) => response.json())
//     .then((data) => {
//       createChart(data.tasks, data.progress, data.colors);
//     });
// }

// document.getElementById('updateButton').addEventListener('click', updateData);

// updateData();

var xValues = [
  'TASK 1',
  'TASK 2',
  'TASK 3',
  'TASK 4',
  'TASK 5',
  'TASK 6',
  'TASK 7',
  'TASK 8',
  'TASK 9',
  'TASK 10',
];
var yValues = [90, 75, 40, 25, 60, 50, 80, 100, 52, 60];
var barColors = '#4aaff7';
Chart.defaults.backgroundColor = '#fff';
Chart.defaults.borderColor = '#fff';
Chart.defaults.color = '#000';
Chart.defaults.font.size = 12;
Chart.defaults.font.family = "'Inter', sans-serif";

new Chart('myChart', {
  type: 'bar',
  data: {
    labels: xValues,
    datasets: [
      {
        backgroundColor: barColors,
        data: yValues,
      },
    ],
  },
  options: {
    legend: { display: true },
    title: {
      display: false,
      text: 'TASK PROGRESS %',
    },
    plugins: {
      legend: {
        labels: {
          font: {
            size: 0,
          },
        },
      },
    },
    indexAxis: 'y',
  },
});
