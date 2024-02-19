console.log("update")

function newWL(){
    window.location.href = '/worklogs/new'
}

function editProfile(){
    window.location.href = '/profile';
}


    // Get the workout data from the server
const workoutData = [
    { week: 'Week 1', count: 5 },
    { week: 'Week 2', count: 8 },
    { week: 'Week 3', count: 3 },
    { week: 'Week 3', count: 4 },

    // Add more data here...
];

// Prepare the data for the chart
const labels = workoutData.map(data => data.week);
const data = workoutData.map(data => data.count);

// Create the chart
const ctx = document.getElementById('myChart').getContext('2d');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'Number of Workouts',
            data: data,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                stepSize: 1
            }
        }
    }
});
