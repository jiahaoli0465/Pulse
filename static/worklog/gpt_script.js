function updateChat(message, isUser) {
    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<div>${isUser ? 'You' : 'Bot'}: ${message}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    let userInput = document.getElementById("user-input");
    if (!userInput.value.trim()) return;

    updateChat(userInput.value, true);

    try {
        // Send data to Flask server
        let response = await fetch('/chatbot/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userInput.value }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        let data = await response.json();
        updateChat(data.reply, false);
    } catch (error) {
        updateChat("Failed to get response from the server.", false);
        console.error("Fetch error: " + error.message);
    }

    userInput.value = "";
}

// Allow pressing "Enter" to send a message
document.getElementById("user-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});