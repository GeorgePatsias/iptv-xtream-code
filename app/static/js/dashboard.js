$(document).ready(function () {

    // Area Chart Example
    var ctx = document.getElementById("myAreaChart");
    var myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["Mar 1", "Mar 2", "Mar 3", "Mar 4", "Mar 5", "Mar 6", "Mar 7", "Mar 8", "Mar 9", "Mar 10", "Mar 11", "Mar 12", "Mar 13"],
            datasets: [{
                label: "Sessions",
                lineTension: 0.3,
                backgroundColor: "rgba(2,117,216,0.2)",
                borderColor: "rgba(2,117,216,1)",
                pointRadius: 5,
                pointBackgroundColor: "rgba(2,117,216,1)",
                pointBorderColor: "rgba(255,255,255,0.8)",
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgba(2,117,216,1)",
                pointHitRadius: 50,
                pointBorderWidth: 2,
                data: [10000, 30162, 26263, 18394, 18287, 28682, 31274, 33259, 25849, 24159, 32651, 31984, 38451],
            }],
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    time: {
                        unit: 'date'
                    },
                    gridLines: {
                        display: false
                    },
                    ticks: {
                        maxTicksLimit: 7
                    }
                },
                y: {
                    ticks: {
                        min: 0,
                        max: 40000,
                        maxTicksLimit: 5
                    },
                    gridLines: {
                        color: "rgba(0, 0, 0, .125)",
                    }
                },
            },
            plugins: {
                legend: {
                    display: false,
                }
            }
        }
    });



    // Bar Chart Example
    var ctx = document.getElementById("myBarChart");
    var data = $("#barChartData").val().split(',').map(Number);
    console.log(data);

    var myBarChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "Octomber", "November", "December"],
            datasets: [{
                label: "Count",
                backgroundColor: "rgba(2,117,216,1)",
                borderColor: "rgba(2,117,216,1)",
                data: data,
            }],
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    time: {
                        unit: 'month'
                    },
                    gridLines: {
                        display: false
                    }
                },
                y: {
                    ticks: {
                        precision: 0
                    },
                    gridLines: {
                        display: true
                    }
                },
            },
            plugins: {
                legend: {
                    display: false,
                }
            }
        }
    });
















});