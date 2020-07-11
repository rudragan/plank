document.addEventListener('DOMContentLoaded', ()=>{
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    let room = 'lounge';
    joinRoom('lounge');



    socket.on('message', data => {

        // Display current message
        if (data.msg) {
            const p = document.createElement('p');
            const span_username = document.createElement('span');
            const span_timestamp = document.createElement('span');
            const br = document.createElement('br')
            // Display user's own message
            if (data.username == username) {
                    p.setAttribute("class", "my-msg");

                    // Username
                    span_username.setAttribute("class", "my-username");
                    span_username.innerText = data.username;

                    // Timestamp
                    span_timestamp.setAttribute("class", "timestamp");
                    span_timestamp.innerText = data.time_stamp;

                    // HTML to append
                    p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML

                    //Append
                    document.querySelector('#display').append(p);
            }
            // Display other users' messages
            else if (typeof data.username !== 'undefined') {
                p.setAttribute("class", "others-msg");

                // Username
                span_username.setAttribute("class", "other-username");
                span_username.innerText = data.username;

                // Timestamp
                span_timestamp.setAttribute("class", "timestamp");
                span_timestamp.innerText = data.time_stamp;

                // HTML to append
                p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;

                //Append
                document.querySelector('#display').append(p);
            }
            // Display system message
            else {
                printSysMsg(data.msg);
            }


        }
        scrollDownChatWindow();
        
    });

   



    document.querySelector('#send_message').onclick = () => {
        socket.send({'msg': document.querySelector("#user_message").value, 
        'username': username, 'room': room });

        document.querySelector('#user_message').value = '';
    }

    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg = `You are already in ${room} room.`
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
        scrollDownChatWindow();
    });

    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});
    }

    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room});

        document.querySelector('#display').innerHTML = ''

        document.querySelector('#user_message').focus()
    }

    function scrollDownChatWindow() {
        var chatWindow = document.querySelector("#display");
        chatWindow.scrollTop = chatWindow.scrollHeight - chatWindow.clientHeight;
    }

    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        document.querySelector('#display').append(p);
        scrollDownChatWindow();

        // Autofocus on text box
        document.querySelector("#user_message").focus();
    }
});

document.addEventListener('DOMContentLoaded', () => {

    let msg = document.querySelector('#user_message');
    msg.addEventListener('keyup', event => {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.querySelector('#send_message').click();
        }
    })
})