console.log("newlog loaded")

const workoutTypeSelect = document.getElementById("workout_type")

workoutTypeSelect.addEventListener("input", updateWorkoutType)

function updateWorkoutType(){
    console.log("type changed")
    const options = {
        method:"POST", 

        body:JSON.stringify({
            data:"data to send here"
        }), 

        headers: {'Content-type': 'application/json; charset=UTF-8'}
    }

    const request = new Request("", options)

    fetch(request)
    .then((response) => {
        if(response.ok){
            console.log("YIPPEE!")

            return response.text()
        } else {
            throw new Error(`something bad happened: ${response.status}`);
        }
    })
    .then((data) => {
        console.log(data)
    })

}