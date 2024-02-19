console.log("update")

function newWL(){
    window.location.href = '/worklogs/new'
}

function editProfile(){
    window.location.href = '/profile';
}


    // Get the workout data from the server
// const workoutData = [
//     { week: 'Week 1', count: 5 },
//     { week: 'Week 2', count: 8 },
//     { week: 'Week 3', count: 3 },
//     { week: 'Week 3', count: 4 },

//     // Add more data here...
// ];

// // Prepare the data for the chart
// const labels = workoutData.map(data => data.week);
// const data = workoutData.map(data => data.count);

// // Create the chart
// const ctx = document.getElementById('myChart').getContext('2d');
// new Chart(ctx, {
//     type: 'bar',
//     data: {
//         labels: labels,
//         datasets: [{
//             label: 'Number of Workouts',
//             data: data,
//             backgroundColor: 'rgba(75, 192, 192, 0.2)',
//             borderColor: 'rgba(75, 192, 192, 1)',
//             borderWidth: 1
//         }]
//     },
//     options: {
//         scales: {
//             y: {
//                 beginAtZero: true,
//                 stepSize: 1
//             }
//         }
//     }
// });

function fetchWorkoutData(userId) {
    // Adjust the URL to match your Flask app's route for fetching workout stats
    fetch(`/api/user/${userId}/worklog-stats`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Workout data:', data);
            updateChart(data);
        })
        .catch(error => {
            console.error('Error fetching workout data:', error);
        });
}


function updateChart(workoutData) {
    const labels = workoutData.map(data => data.week);
    // Use the .map() function to enforce a maximum count of 8 per week
    const dataCounts = workoutData.map(data => Math.min(data.count, 7));

    const ctx = document.getElementById('myChart').getContext('2d');



    window.myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Monthly Workouts',
                data: dataCounts,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    stepSize: 1,
                    // Explicitly define the maximum value if you want to ensure the scale always goes up to 8
                    max: 7
                }
            },
            // Adding this option to maintain bar thickness regardless of the amount of data
            // maintainAspectRatio: false,
            // responsive: true,
        }
    });
}


const userId = document.querySelector('#profile').dataset.userId;
console.log(userId)
fetchWorkoutData(userId);


function fetchYearlyWorkoutData(userId) {
    // Adjust the URL to match your Flask app's route for fetching yearly workout stats
    fetch(`/api/user/${userId}/worklog-year-stats`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Yearly workout data:', data);
            updateYearlyChart(data);
        })
        .catch(error => {
            console.error('Error fetching yearly workout data:', error);
        });
}

function updateYearlyChart(workoutData) {
    // Directly use the 'month' value from each data point as the label
    const labels = workoutData.map(data => data.month);
    const dataCounts = workoutData.map(data => data.count);

    const ctx = document.getElementById('myYearlyChart').getContext('2d'); // Ensure this ID matches your <canvas> element



    window.myYearlyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Yearly Workouts',
                data: dataCounts,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    stepSize: 1,
                    max: 35 // Adjust max value as necessary
                }
            }
        }
    });
}


console.log('Fetching yearly workout data for user ID:', userId);
fetchYearlyWorkoutData(userId);
