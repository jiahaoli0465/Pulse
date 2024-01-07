const newExerciseBtn = document.querySelector('#newExercise-btn');
const addExerciseDiv = document.querySelector('#newExerciseFormDiv');
const newExerciseForm = document.querySelector('#newExerciseForm');
const exitCreate = document.querySelector('#exitCreate');
const exitSetButtons = document.querySelectorAll('.exitSet');
const editSetButtons = document.querySelectorAll('.set-edit')
const newSetFormDiv = document.querySelector('#newSetFormDiv');
const newSetForm = document.querySelector('#newSetForm');
const editForm = document.querySelector("#editSetFormDiv")
const editSetForm = document.querySelector('#editSetForm')
const logsContainer = document.querySelector('.logsContainer'); 
const worklog_id = document.querySelector('.worklog-container').getAttribute('data-worklog_id');
let currentExerciseId = null;
let currentSetId = null;

document.addEventListener('DOMContentLoaded', async function() { 
        
    newExerciseBtn.addEventListener('click', function(){
        addExerciseDiv.classList.remove('hidden');
    });

    exitCreate.addEventListener('click', function(){
        addExerciseDiv.classList.add('hidden');
    });

    exitSetButtons.forEach(button => {
        button.addEventListener('click', function() {
            console.log("listener");
            button.parentNode.classList.add('hidden');
        });
    });
    


    function appendNewExercise(name, exercise_id) {
        const template = newExerciseTemplate(name, exercise_id);
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = template.trim();
        logsContainer.appendChild(tempDiv.firstChild);
    }
    
    function appendNewSet(num, weight, reps, set_id, logContainer) {
        const setTemplate = newSetTemplate(num, weight, reps, set_id);
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = setTemplate.trim();
        logContainer.appendChild(tempDiv.firstChild);
    }

    
    function newExerciseTemplate(exerciseName, exerciseId) {
        let btnId = exerciseId;
        return `            
        <div class="log">
            <div class="log-container" data-exercise_id = ${exerciseId}>
                <div class="log-title"><h4>${exerciseName}</h4> <div class="btns"><button data-btnId = ${btnId} class="add">+</button><button class="dlt">x</button></div></div>
                <div class="log-content" data-exerciseId = ${exerciseId}>

                </div>
            </div>
        </div>`;
    }

    function newSetTemplate(num, weight, reps, id) {
        return `
        <div class="set">
            <div class="set-content">
                <p data-setIdContainer = ${id}>Set ${num} - ${weight}lbs - ${reps} reps</p>
                <div class="set-btns"><button data-setId = ${id} class="set-edit"><i class="fa-solid fa-pen-to-square"></i></button></div>
            </div>
        </div>
        `;
    }


    newExerciseForm.addEventListener('submit', function(e) {
        e.preventDefault();
        let name = document.querySelector('#exerciseName').value; 
        console.log(name);
    
        axios.post(`/worklog/${worklog_id}/exercise`, {
            name: name
        })
        .then((response) => {
            console.log(response);
            const exercise_id = response.data.exercise_id;
            console.log("Received exercise ID:", exercise_id);
    
            appendNewExercise(name, exercise_id); // Use the new function here
            addExerciseDiv.classList.add('hidden');
        })
        .catch((error) => {
            console.log(error);
        });
        newExerciseForm.reset();
    });
    

    editSetForm.addEventListener('submit', function(e) {
        e.preventDefault();
        console.log('current set id: ' + currentSetId);
        console.log('current exercise id: ' + currentExerciseId);
    
        const num = document.querySelector('#edit-num').value;
        const weight = document.querySelector('#edit-weight').value;
        const reps = document.querySelector('#edit-rep').value;
        console.log(num, weight, reps)
    
        axios.patch(`/worklog/${worklog_id}/exercise/${currentExerciseId}/set/${currentSetId}`, {
            setNum: num,
            setWeight: weight,
            setReps: reps
        })
        .then((response) => {
            console.log(response);
            let setContainer = document.querySelector(`[data-setidcontainer="${currentSetId}"]`);
            console.log(setContainer)
            setContainer.innerHTML = `Set ${num} - ${weight}lbs - ${reps} reps`; // Update existing set element
    
            currentExerciseId = null;
            currentSetId = null;
        })
        .catch((error) => {
            console.log(error);
        });
    
        editSetForm.reset();
        editSetForm.parentElement.classList.add('hidden');
    });
    
    
    newSetForm.addEventListener('submit', function(e) {
        e.preventDefault();
        console.log('current exerciseId: ' + currentExerciseId);
    
        const logContainer = document.querySelector(`[data-exerciseId="${currentExerciseId}"]`);
        const num = document.querySelector('#set-num').value;
        const weight = document.querySelector('#set-weight').value;
        const reps = document.querySelector('#set-rep').value;
    
        axios.post(`/worklog/${worklog_id}/exercise/${currentExerciseId}/set`, {
            setNum: num,
            setWeight: weight,
            setReps: reps
        })
        .then((response) => {
            console.log(response);
            const set_id = response.data.set_id;
            console.log(set_id);
    
            appendNewSet(num, weight, reps, set_id, logContainer); 
    
            currentExerciseId = null;
        })
        .catch((error) => {
            console.log(error);
        });
    
        newSetForm.reset();
        newSetFormDiv.classList.add('hidden');
    });
    

    logsContainer.addEventListener('click', function(event) {
    // Check if the clicked element has the class 'dlt'
        if (event.target.classList.contains('dlt')) {
            // Show confirmation dialog
            
            if (confirm('Are you sure you want to delete this?')) {
                // Remove the parent element of the clicked button
                const id = event.target.parentElement.parentElement.parentElement.parentElement.querySelector('.log-container').getAttribute('data-exercise_id');
                console.log(id)

                axios.delete(`/worklog/${worklog_id}/exercise/${id}`)
                .then((response) => {
                    console.log(response)
                    event.target.parentElement.parentElement.parentElement.parentElement.remove()

                })
                .catch((error) => {
                    console.log(error)
                  });
            }
        }
        if (event.target.classList.contains('add')) {
            // Show confirmation dialog
            currentExerciseId = event.target.getAttribute('data-btnId');
            const id = event.target.parentElement.parentElement.parentElement.parentElement.querySelector('.log-container').getAttribute('data-exercise_id');
            console.log(id)
            console.log(currentExerciseId);
            newSetFormDiv.classList.remove('hidden');     

        }

        if (event.target.classList.contains('set-edit') || event.target.parentElement.classList.contains('set-edit') ) {
            // Show confirmation dialog
            console.log('clicked')

            let setId = null;
            if (event.target.classList.contains('set-edit')) {
                setId = event.target.getAttribute('data-setid');
                console.log(event.target.parentElement.parentElement.parentElement.parentElement.getAttribute('data-exerciseid'));
                currentExerciseId = event.target.parentElement.parentElement.parentElement.parentElement.getAttribute('data-exerciseid');
            } else {
                console.log(event.target.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-exerciseid'));
                currentExerciseId = event.target.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('data-exerciseid');
                setId = event.target.parentElement.getAttribute('data-setid');
            }
            console.log(setId);
            currentSetId = setId;
            editForm.classList.remove('hidden')
        }
    });

    // deleteButtonEventListener()
});



// function deleteButtonEventListener(){
//     document.querySelector("#deleteSetBtn").addEventListener('click', () => {
//         axios.delete(`/worklog/${worklog_id}/exercise/${currentExerciseId}/set/${currentSetId}`)
//         .then((response) => {
//             document.querySelector(`[data-setidcontainer="${currentSetId}"]`).parentElement.parentElement.remove()
//         })
//         .catch(error => {
//             console.log(error)
//         })
//     })
// }

