console.log("new")
const form_container = document.getElementById("form-container");
const form_button = document.getElementById("form-button");
form_button.addEventListener("click", () => {
    console.log("pressed")
    form_container.appendChild(document.createElement("input"));
})