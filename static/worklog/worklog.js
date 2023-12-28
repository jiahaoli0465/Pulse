const newExerciseBtn = document.querySelector('#newExercise-btn');
const addExerciseDiv = document.querySelector('#newExerciseFormDiv');
const newExerciseForm = document.querySelector('#newExerciseForm');
const exitCreate = document.querySelector('#exitCreate');
const exitSet = document.querySelector('#exitSet');
const newSetFormDiv = document.querySelector('#newSetFormDiv');
const newSetForm = document.querySelector('#newSetForm');
let logsContainer = document.querySelector('.logsContainer'); 
let currentExerciseId = null;

// async function sendNewExerciseRequest(exerciseName){

//     console.log(`send ${exerciseName}`)
//     const options = {
//         method:"POST", 

//         body:JSON.stringify({
//             exerciseName:exerciseName
//         }), 

//         headers: {'Content-type': 'application/json; charset=UTF-8'}
//     }
    
//     const url = "";
//     const request = new Request(url, options)

//     await fetch(request)
//     .then((response) => {
//         if(response.ok){
//             console.log("Request successful")

//             return response.text()
//         } else {
//             throw new Error(`something bad happened: ${response.status}`);
//         }
//     })
//     .then((data) => {
//         console.log(data)
//         // here you would add something that handles the data from a json preferably but there's nothing here so have a skeleton instead
//         for(let thing in data){
//             //document.getElementById("container for workouts").innerHtml+= "<PUT HTML HERE>"
//         }
//     })
// }

document.addEventListener('DOMContentLoaded', async function() { 
        
    newExerciseBtn.addEventListener('click', function(){
        addExerciseDiv.classList.remove('hidden');
    });

    exitCreate.addEventListener('click', function(){
        addExerciseDiv.classList.add('hidden');
    });

    exitSet.addEventListener('click', function(){
        newSetFormDiv.classList.add('hidden');
    });

    newSetFormDiv
    function newExerciseTemplate(exerciseName, exerciseId) {
        let btnId = exerciseId;
        return `            
        <div class="log">
            <div class="log-container">
                <div class="log-title"><h4>${exerciseName}</h4> <div class="btns"><button data-btnId = ${btnId} class="add">+</button><button class="dlt">x</button></div></div>
                <div class="log-content" data-exerciseId = ${exerciseId}>

                </div>
            </div>
        </div>`;
    }

    function newSetTemplate(num, weight, reps) {
        return `
        <div class="set">
            <div class="set-content">
                <p>Set ${num} - ${weight}lbs - ${reps} reps</p>
                <div class="set-btns"><button class="set-edit"><i class="fa-solid fa-pen-to-square"></i></button></div>
            </div>
        </div>
        `;

    
    }
    // TEMPORARY TESTING
    let count = 2;
    /////////////////////
    newExerciseForm.addEventListener('submit', function(e) {
        e.preventDefault();
        let exerciseName = document.querySelector('#exerciseName').value; 
        console.log(exerciseName);








        // let res = sendNewExerciseRequest(exerciseName)

        const template = newExerciseTemplate(exerciseName, count);
        count += 1;
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = template.trim(); 
        logsContainer.appendChild(tempDiv.firstChild);
        addExerciseDiv.classList.add('hidden');
    });
    
    newSetForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const num = document.querySelector('#set-num').value;
        const weight = document.querySelector('#set-weight').value;
        const reps = document.querySelector('#set-rep').value;
        
        //send request to server

        const setTemplate = newSetTemplate(num, weight, reps);
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = setTemplate.trim(); 
        const logContainer = document.querySelector(`[data-exerciseId="${currentExerciseId}"]`);
    
        if (logContainer) {
            // Append the new set to the log-content div
            console.log('im here')
            logContainer.appendChild(tempDiv.firstChild);
        }
    
        // Reset the form and currentExerciseId
        newSetForm.reset();
        currentExerciseId = null;
        newSetFormDiv.classList.add('hidden');
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
        if (event.target.classList.contains('add')) {
            // Show confirmation dialog
            currentExerciseId = event.target.getAttribute('data-btnId');
            newSetFormDiv.classList.remove('hidden');

                
            
        }


    
});
});