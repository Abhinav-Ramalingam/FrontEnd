document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('messageForm');

    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevents the form from submitting the normal way (i.e., reloading the page)

        var formData = new FormData(form);
        var messageInput = document.getElementById('messageInput');
        var message = messageInput.value;

        var payload = {
            topic: formData.get('topic'),
            username: formData.get('username'),
            deviceID: "testID",  // You can modify this or set dynamically
            message: formData.get('message')
        };

        console.log(payload)

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/send_message/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    // Clear the input field
                    messageInput.value = '';
                    // Optionally, append the new message to the chat display dynamically
                    appendMessage(payload);  // Call function to display the message
                } else {
                    console.error("Error sending message:", xhr.responseText);
                }
            }
        };

        // Send the payload as JSON
        xhr.send(JSON.stringify(payload));
    });

    function appendMessage(payload) {
        var messagesDiv = document.getElementById('messages');

        var newMessageDiv = document.createElement('div');
        newMessageDiv.className = payload.username === 'test' ? 'chat chat-start' : 'chat chat-end';

        var messageHtml = `
            <div class="chat-image avatar">
                <div class="w-10 rounded-full">
                    <img alt="${payload.username}'s avatar" src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" />
                </div>
            </div>
            <div class="chat-header">
                ${payload.username}
                <time class="text-xs opacity-50">Now</time>
            </div>
            <div class="chat-bubble">${payload.message}</div>
        `;

        newMessageDiv.innerHTML = messageHtml;
        messagesDiv.appendChild(newMessageDiv);

        // Scroll to the bottom of the chat
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
});
