document.addEventListener('DOMContentLoaded', () => {
    const inputField = document.querySelector('#chatInput');
    const sendButton = document.querySelector('#inputSection button');
    const chat = document.querySelector('#chatContent');
    const loader = document.querySelector('.loader-container');
    const chatBtn = document.getElementById('chatBtn');
    const chatSection = document.getElementById('chatSection');
    const userId = chatSection.getAttribute('data-user-id');
    sendUserHistory();


    const exitButton = document.querySelector('#chatHeader button');
    chatSection.classList.add('hidden');

    chatBtn.addEventListener('click', function() {
        chatSection.classList.toggle('hidden');
    });

    exitButton.addEventListener('click', function() {
        chatSection.classList.add('hidden');
    });

    function scrollToBottom(element) {
        element.scrollTop = element.scrollHeight;
    }

    function addToChat(input, isBotMessage = false) {
        if (!chat) {
            console.error('Chat element not found!');
            return;
        }

        const messageClass = isBotMessage ? 'botText' : 'userText';
        const messageContainerClass = isBotMessage ? 'message bot-message' : 'message user-message';

        const messageElement = document.createElement('div');
        messageElement.className = messageContainerClass;

        const textElement = document.createElement('div');
        textElement.className = messageClass;
        textElement.textContent = input;

        messageElement.appendChild(textElement);
        chat.appendChild(messageElement);

        // Scroll to the new message
        scrollToBottom(chat);
    }

    function showLoader() {
        loader.style.display = 'flex';
    }

    function hideLoader() {
        loader.style.display = 'none';
    }

    async function sendMessage() {
        const message = inputField.value.trim();
        if (!message) {
            // alert("Please enter a message.");
            return;
        }
        if (message.length > 500) {
            alert("Message is too long. Please limit it to 500 characters.");
            return;
        }

        addToChat(message); // User message
        inputField.value = '';
        showLoader();

        try {
            // Send data to Flask server using Axios
            const response = await axios.post('/chatbot/chat', { message: message });

            hideLoader();
            addToChat(response.data.reply, true); // Bot message

        } catch (error) {
            addToChat("Failed to get response from the server.", true);
            hideLoader();
            console.error("Axios error: " + error);
        }



    }

    async function sendHistory() {
        const history = await axios.get(`/api/user/${userId}/worklogs`)
        if (!history) {
            // alert("Please enter a message.");
            return;
        }


        addToChat(JSON.stringify(history.data)); // User message
        // inputField.value = '';
        showLoader();

        try {
            // Send data to Flask server using Axios
            const response = await axios.post('/chatbot/chat', { message: JSON.stringify(history.data) });

            hideLoader();
            addToChat(response.data.reply, true); // Bot message

        } catch (error) {
            addToChat("Failed to get response from the server.", true);
            hideLoader();
            console.error("Axios error: " + error);
        }



    }



    sendButton.addEventListener('click', sendMessage);

    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });


    async function sendUserHistory(){
        const chatSection = document.getElementById('chatSection');
        const userId = chatSection.getAttribute('data-user-id');
    
        if (userId == 0) {
            console.log('no user found')
            return;
        }
        const history = await axios.get(`/api/user/${userId}/worklogs`)
        
        console.log(history.data);
        try {
            showLoader();
    
            let guide = 'this is the server sending you the user history so you can help guide the user for further questions. Do not respond to this message, just keep it to be referenced';
            const response = await axios.post('/chatbot/chat', { message: `${guide} ${JSON.stringify(history.data)}`});
            console.log(response.data);
            hideLoader();
    
        }
        catch (error) {
            console.error("Axios error: " + error);
            hideLoader();
    
    
        }
    
    }

});

