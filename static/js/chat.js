
const sendButton = document.getElementById('sendButton');
const receiveButton = document.getElementById('receiveButton');
const messageInput = document.getElementById('messageInput');
const messagesDiv = document.getElementById('messages');

sendButton.addEventListener('click', function () {
    const message = messageInput.value.trim();
    if (message) {
        addMessage(message, true); // Add user message
        messageInput.value = ''; // Clear the input field
    }
});

receiveButton.addEventListener('click', function () {
    const message = messageInput.value.trim();
    if (message) {
        addMessage(message, false); // Add received message
        messageInput.value = ''; // Clear the input field
    }
});

function addMessage(message, isUserMessage) {
    const messageElement = document.createElement('div');
    messageElement.className = `chat ${isUserMessage ? 'chat-end' : 'chat-start'}`;

    messageElement.innerHTML = `
            <div class="chat-image avatar">
                <div class="w-10 rounded-full">
                    <img
                      alt="${isUserMessage ? 'User Avatar' : 'Other User Avatar'}"
                      src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp" />
                </div>
            </div>
            <div class="chat-header">
                ${isUserMessage ? 'You' : 'Other User'}
                <time class="text-xs opacity-50">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</time>
            </div>
            <div class="chat-bubble">${message}</div>
            <div class="chat-footer opacity-50">Delivered</div>
        `;

    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to the bottom
}
