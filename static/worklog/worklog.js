const newExerciseBtn = document.querySelector('#newExercise-btn');
const addExerciseDiv = document.querySelector('#newExerciseFormDiv');
const newExerciseForm = document.querySelector('#newExerciseForm');
const exitCreate = document.querySelector('#exitCreate');


    


newExerciseBtn.addEventListener('click', function(){
    addExerciseDiv.classList.remove('hidden');
});
exitCreate.addEventListener('click', function(){
    addExerciseDiv.classList.add('hidden');
});


newExerciseForm.addEventListener('submit', function(e){
    e.preventDefault();
    let exerciseName = document.querySelector('#exerciseName').value; 
    
})