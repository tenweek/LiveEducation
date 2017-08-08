<template>
    <div class="chat-board">
        chat board
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
            document.getElementById('msgInput').value = ''
            this.socket.emit('message', msg, this.id + '.1')
        }
    },
    mounted: function () {
        this.socket = io.connect('http://localhost:9000')
        this.socket.emit('join', this.id + '.1')
        this.socket.on('message', function (msg) {
            let ul = document.getElementById('messages')
            let li = document.createElement("li")
            li.innerText = msg
            ul.insertBefore(li, ul.childNodes[ul.childNodes.length])
        })
    }
}
</script>
