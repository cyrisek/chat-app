const chatSocket = new WebSocket(
    'wss://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);
function scrollDown() {
    // Get the current scroll position

    const chatHistory = document.querySelector('.chat-history');

    // Scroll to the new position
    chatHistory.scrollTop = chatHistory.scrollHeight;
    chatHistory.scrollIntoView({ behavior: "smooth" });

}
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log('Message received:', e.data);
    const ul = document.getElementById('chatbox');
    if (parseInt(data.user_id) === userID) {
        ul.innerHTML += ` <li class="clearfix">
        <div class="message-data">
            <span class="message-data-time">Just now.</span>
        </div>
        <div class="message my-message">${data.message}</div>
    </li>`;
    } else {
        ul.innerHTML += `<li class="clearfix">
            <div class="message-data text-right">
                <span class="message-data-time">Just now.</span>
            </div>
            <div class="message other-message float-right">${data.message}</div>
        </li>`;
    }
    scrollDown();


};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
    const newDiv = document.createElement('div');
    newDiv.innerHTML = `<div class="alert alert-success" role="alert">
        <p>Connection lost, try refreshing the page</p>
    </div>`;
    const body = document.querySelector('.container');
    body.appendChild(newDiv);
};

document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    if (message.trim() === '') {
        return
    }
    const chat_id = roomName
    const user_id = userID
    chatSocket.send(JSON.stringify({
        'message': message,
        'chat_id': chat_id,
        'user_id': user_id,
    }));
    messageInputDom.value = '';
};

window.addEventListener('load', () => {
    scrollDown();
});
