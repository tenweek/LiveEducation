<template>
    <div class="chat-board">
        <ul id="messages"></ul>
        <form action="">
            <input id="msgInput" autocomplete="off" />
            <button @click="sendMsg">Send</button>
        </form>
    </div>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
import * as io from 'socket.io-client'
export default {
    name: 'chat-board',
    props: ['id'],
    data: function () {
        return {
            socket: ''
        }
    },
    methods: {
        sendMsg: function () {
            let msg = document.getElementById('msgInput').value
            if (msg === '') {
                return
            }
            document.getElementById('msgInput').value = ''
            this.socket.emit('message', msg, this.id + '.1')
        }
    },
    mounted: function () {
        this.socket = io.connect('http://localhost:9000')
        this.socket.emit('join', this.id + '.1')
        this.socket.on('message', function (msg) {
            let ul = document.getElementById('messages')
            let li = document.createElement('li')
            li.innerText = msg
            ul.insertBefore(li, ul.childNodes[ul.childNodes.length])
            let scroll = document.getElementById('messages')
            scroll.scrollTop = scroll.scrollHeight
        })
    }
}
</script>

<style scope>
* {
    overflow: hidden;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

form {
    position: absolute;
    bottom: 30px;
}

.chat-board {
    width: 394px;
    height: 294px;
}

form input {
    width: 325px;
    height: 30px;
}

form button {
    position: relative;
    left: -4.5px;
    width: 70px;
    height: 30px;
    background: rgb(130, 224, 255);
    border: none;
}

#messages {
    list-style-type: none;
    height: 264.5px;
    width: 395.5px;
    overflow-y: auto;
    margin: 0;
    padding: 0;
    padding-left: 10px;
    padding-top: 5px;
}

#messages ul,
#messages li {
    width: 373px;
}

#messages li {
    word-break: break-all;
    word-wrap: break-word;
    text-align: left;
    padding: 2px 0px;
    width: 373px;
}
</style>
