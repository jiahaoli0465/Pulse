const newExerciseBtn = document.querySelector('#newExercise-btn');
const addExerciseDiv = document.querySelector('#newExerciseFormDiv');
const newExerciseForm = document.querySelector('#newExerciseForm');
const exitCreate = document.querySelector('#exitCreate');

let logsContainer = document.querySelector('.logsContainer'); 
    
async function sendNewExerciseRequest(exerciseName){

    console.log(`send ${exerciseName}`)
    const options = {
        method:"POST", 

        body:JSON.stringify({
            exerciseName:exerciseName
        }), 

        headers: {'Content-type': 'application/json; charset=UTF-8'}
    }
    
    const url = "";
    const request = new Request(url, options)

    await fetch(request)
    .then((response) => {
        if(response.ok){
            console.log("Request successful")

            return response.text()
        } else {
            throw new Error(`something bad happened: ${response.status}`);
        }
    })
    .then((data) => {
        console.log(data)
        // here you would add something that handles the data from a json preferably but there's nothing here so have a skeleton instead
        for(let thing in data){
            //document.getElementById("container for workouts").innerHtml+= "<PUT HTML HERE>"
        }
    })
}

document.addEventListener('DOMContentLoaded', async function() { 
        
    newExerciseBtn.addEventListener('click', function(){
        addExerciseDiv.classList.remove('hidden');
    });
    exitCreate.addEventListener('click', function(){
        addExerciseDiv.classList.add('hidden');
    });
    function newExerciseTemplate(exerciseName) {
        return `            
        <div class="log">
            <div class="log-container">
                <div class="log-title"><h4>${exerciseName}</h4> <div class="btns"><button class="add">+</button><button class="dlt">x</button></div></div>
                <div class="log-content">

                </div>
            </div>
        </div>`;
    }
    
    newExerciseForm.addEventListener('submit', function(e) {
        e.preventDefault();
        let exerciseName = document.querySelector('#exerciseName').value; 
        console.log(exerciseName);
        const template = newExerciseTemplate(exerciseName);

        // Convert the string to a DOM element
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = template.trim(); 


        logsContainer.appendChild(tempDiv.firstChild);
        addExerciseDiv.classList.add('hidden');


        sendNewExerciseRequest(exerciseName)

    });




    logsContainer.addEventListener('click', function(event) {
    // Check if the clicked element has the class 'dlt'
    if (event.target.classList.contains('dlt')) {
        // Show confirmation dialog
        if (confirm('Are you sure you want to delete this?')) {
            // Remove the parent element of the clicked button
            event.target.parentElement.parentElement.parentElement.parentElement.remove();
        }
    }
});
});