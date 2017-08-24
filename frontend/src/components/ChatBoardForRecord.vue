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
        <Button id="send-btn" slot="append" disabled>发送</Button>
        </Input>
    </div>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
/**
 * 实现聊天室的复现，
 * 作为子组件插入录播间页面。
 *
 * @module ChatBoardForRecord
 * @class ChatBoardForRecord
 */
import * as io from 'socket.io-client'
export default {
    name: 'chat-board',
    props: ['userAccount', 'roomId', 'chatBoardHeight'],
    data: function () {
        return {
            /**
             * 表示客户端，负责监听服务器传来的消息
             *
             * @attribute socket
             * @type Object
             * @default ''
             */
            socket: '',
            /**
             * 存储发言记录
             *
             * @attribute messages
             * @type Array
             * @default []
             */
            messages: []
        }
    },
    /**
     * mounted函数，初始化相关数据，客户端负责监听服务器传来的消息。
     *
     * @method mounted
     */
    mounted: function () {
        let self = this
        self.socket = io.connect('http://localhost:9000')
        self.socket.emit('joinTest', self.roomId, 'chatboard')
        self.socket.on('chatroom', function (data) {
            self.messages.push({
                'msg': data['message'],
                'isTeacher': data['isTeacher']
            })
            let scroll = document.getElementById('messages')
            scroll.scrollTop = scroll.scrollHeight
        })
        document.getElementById('messages').style.height = (this.chatBoardHeight - 32) + 'px'
    },
    watch: {
        chatBoardHeight: function (newVal, oldVal) {
            document.getElementById('messages').style.height = (newVal - 32) + 'px'
        }
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

#messages {
    overflow: auto;
}
</style>
