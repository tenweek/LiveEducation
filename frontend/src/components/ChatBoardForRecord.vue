<template>
    <div class="chat-board">
        <div id="messages">
            <div v-for="message in messages">
                <Dropdown class="set-left" trigger="click">
                    <template v-if="message['isTeacher']">
                        <button class="message-bold">
                            {{ message['msg'] }}
                        </button>
                    </template>
                    <template v-else>
                        <button class="message">
                            {{ message['msg'] }}
                        </button>
                    </template>
                </Dropdown>
            </div>
        </div>
        <Input>
        <Button id="send-btn" slot="append">发送</Button>
        </Input>
    </div>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
import * as io from 'socket.io-client'
export default {
    name: 'chat-board',
    props: ['roomId'],
    data: function () {
        return {
            socket: '',
            messages: []
        }
    },
    mounted: function () {
        let self = this
        self.socket = io.connect('http://localhost:9000')
        self.socket.emit('joinTest', 888)
        self.socket.on('chatroom', function (data) {
            self.messages.push({
                'msg': data['message'],
                'isTeacher': data['isTeacher']
            })
            let scroll = document.getElementById('messages')
            scroll.scrollTop = scroll.scrollHeight
        })
    }
}
</script>

<style scoped>
* {
    overflow: hidden;
}

.chat-board {
    width: 100%;
    height: 100%;
    position: relative;
}

.message,
.message-bold {
    background-color: Transparent;
    border-style: None;
    outline: none;
    word-wrap: break-word !important;
    word-break: break-all !important;
    white-space: normal !important;
    text-align: left;
    padding-top: 2px;
    width: 100%;
}

.message-bold {
    font-weight: bold;
}

.set-left {
    float: left;
    padding-left: 5px;
}

#send-btn {
    color: #6088BB;
    background-color: #9EF4E6;
}

#send-btn:hover {
    border-color: #12CC94;
}

#messages {
    overflow: auto;
    height: 91%;
}
</style>
