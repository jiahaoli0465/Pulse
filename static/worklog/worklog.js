// Select DOM elements
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
const postForm = document.getElementById('newPostForm');
const postBtn = document.getElementById('postBtn');




document.addEventListener('DOMContentLoaded', function() { 

    // getWorklogJson();


    //globalish variables for form submisstions
    let currentExerciseId = null;
    let currentSetId = null;
        
    newExerciseBtn.addEventListener('click', function(){
        addExerciseDiv.classList.remove('hidden');
    });

    postBtn.addEventListener('click', function(){
        document.getElementById('PostDiv').classList.remove('hidden');
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
        const name = document.querySelector('#exerciseName').value;
    
        createExercise(name).then(exercise_id => {
            console.log('created exercise: ' + exercise_id);
            appendNewExercise(name, exercise_id);
            addExerciseDiv.classList.add('hidden');
        }).catch(error => {
            console.error("Failed to create exercise:", error);
        });
    
        newExerciseForm.reset();
    });
    
    function createExercise(name) {
        return axios.post(`/worklog/${worklog_id}/exercise`, { name: name })
            .then(response => response.data.exercise_id);
    }
    

    editSetForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const num = document.querySelector('#edit-num').value;
        const weight = document.querySelector('#edit-weight').value;
        const reps = document.querySelector('#edit-rep').value;
    
        updateSet(currentExerciseId, currentSetId, num, weight, reps)
            .then(() => {
                console.log('updated...')
                updateSetDOM(currentSetId, num, weight, reps);
                currentExerciseId = null;
                currentSetId = null;
            })
            .catch(error => {
                console.error("Failed to update set:", error);
            });
    
        editSetForm.reset();
        editSetForm.parentElement.classList.add('hidden');
    });
    
    function updateSet(exerciseId, setId, num, weight, reps) {
        return axios.patch(`/worklog/${worklog_id}/exercise/${exerciseId}/set/${setId}`, {
            setNum: num,
            setWeight: weight,
            setReps: reps
        });
    }
    
    function updateSetDOM(setId, num, weight, reps) {
        let setContainer = document.querySelector(`[data-setidcontainer="${setId}"]`);
        setContainer.innerHTML = `Set ${num} - ${weight}lbs - ${reps} reps`;
    }
    
    
    
    newSetForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const num = document.querySelector('#set-num').value;
        const weight = document.querySelector('#set-weight').value;
        const reps = document.querySelector('#set-rep').value;
    
        createSet(currentExerciseId, num, weight, reps)
            .then(set_id => {
                console.log('created set: ' + set_id);
                appendNewSet(num, weight, reps, set_id, document.querySelector(`[data-exerciseId="${currentExerciseId}"]`));
                currentExerciseId = null;
            })
            .catch(error => {
                console.error("Failed to create set:", error);

            });
    
        newSetForm.reset();
        newSetFormDiv.classList.add('hidden');
    });
    
    function createSet(exerciseId, num, weight, reps) {
        return axios.post(`/worklog/${worklog_id}/exercise/${exerciseId}/set`, {
            setNum: num,
            setWeight: weight,
            setReps: reps
        }).then(response => response.data.set_id);
    }
    
    
    // Handles click events on the logs container.
    logsContainer.addEventListener('click', function(event) {
        // Delete exercise if 'dlt' class is present in the target element.
        if (event.target.classList.contains('dlt')) {
            handleDeleteClick(event);
        } 
        // Handle adding a set if 'add' class is present.
        else if (event.target.classList.contains('add')) {
            handleAddClick(event);
        } 
        // Handle set editing if 'set-edit' class is present.        
        else if (event.target.classList.contains('set-edit') || event.target.parentElement.classList.contains('set-edit')) {
            handleSetEditClick(event);
        }
    });

    // Handles the edit action for a set.
    function handleSetEditClick(event) {
        const editButton = event.target.classList.contains('set-edit') ? event.target : event.target.parentElement;
        const setId = editButton.getAttribute('data-setid');
        const exerciseContainer = editButton.closest('.log-container');
        console.log('selected set id: ', setId);
    
        if (exerciseContainer) {
            currentExerciseId = exerciseContainer.getAttribute('data-exercise_id');
            currentSetId = setId;
            editForm.classList.remove('hidden');
        } else {
            console.error("Could not find exercise container for editing set");
        }
    }
    
    // Handles the add action for a set.
    function handleAddClick(event) {
        currentExerciseId = event.target.getAttribute('data-btnId');
        const exerciseId = getExerciseId(event.target);
        console.log('Adding to exercise ID:', exerciseId);
        if (exerciseId) {
            currentExerciseId = exerciseId;
            newSetFormDiv.classList.remove('hidden');
        } else {
            console.error("Exercise ID not found for adding set");
        }
    }

    // Handles the delete action for an exercise.
    function handleDeleteClick(event) {
        if (confirm('Are you sure you want to delete this?')) {
            const exerciseId = getExerciseId(event.target);
            console.log('deleting id: ', exerciseId);
            if (exerciseId) {
                deleteExercise(exerciseId, event.target);
            } else {
                console.error("Exercise ID not found");
            }
        }
    }

    // Retrieves the exercise ID from a given element.    
    function getExerciseId(element) {
        const logContainer = element.closest('.log-container');
        return logContainer ? logContainer.getAttribute('data-exercise_id') : null;
    }

     // Performs the delete operation for an exercise.   
    function deleteExercise(exerciseId, targetElement) {
        const logContainer = targetElement.closest('.log-container');
        if (!logContainer) {
            console.error("Log container not found");
            return;
        }
    
        axios.delete(`/worklog/${worklog_id}/exercise/${exerciseId}`)
            .then(response => {
                console.log(response);
                console.log(exerciseId + ' deleted');

                logContainer.parentElement.remove();
            })
            .catch(error => {
                console.error("Failed to delete exercise:", error);
            });
    }


    //this handles deleting a set for any exercise.
    deleteButtonEventListener()

    function deleteButtonEventListener(){
        document.querySelector("#deleteSetBtn").addEventListener('click', (e) => {
            e.preventDefault();
            console.log('trying to delete set id: ', currentSetId)
            if (confirm('delete this set?')) {
                axios.delete(`/worklog/${worklog_id}/exercise/${currentExerciseId}/set/${currentSetId}`)
                .then((response) => {
                    document.querySelector(`[data-setidcontainer="${currentSetId}"]`).parentElement.parentElement.remove()
                    editSetForm.parentElement.classList.add('hidden');
                    currentSetId = null;
                })
                .catch(error => {
                    console.log(error)
                })

            }

        })
    }


    postForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission

        const message = document.getElementById('message').value;
        const worklogId = worklog_id; // You need to provide a way to set this

        axios.post('/api/posts/new', {
            message: message,
            worklog_id: worklogId
        })
        .then(function(response) {
            console.log(response.data); // Handle success
            alert('Post created successfully!');
            document.getElementById('message').value = ''; // Clear the form
            document.getElementById('PostDiv').classList.add('hidden');

            // Optionally hide the form or give other visual feedback
        })
        .catch(function(error) {
            console.error(error); // Handle error
            document.getElementById('PostDiv').classList.add('hidden');

            alert('Failed to create post. ' + error.message);
        });
    });


    document.getElementById('exitPost').addEventListener('click', function() {
        document.getElementById('PostDiv').classList.add('hidden');
    });
    
});

// function getWorklogJson(){
//     axios.get(`/api/worklog/${worklog_id}`)
//     .then(response=>{
//         console.log(response.data)

//         axios.post(`/chatbot/chat`, response.data).then(response=>{
//             console.log("chat message: " + response)
//         })
//     })
// }






