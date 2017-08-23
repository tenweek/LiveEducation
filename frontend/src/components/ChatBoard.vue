<template>
    <Card id="chatboard-card">
        <div id="chat-board">
            <div id="messages">
                <div v-for="message in messages">
                    <Dropdown class="set-left" trigger="click" @on-click="teacherDoing">
                        <template v-if="message['isTeacher']">
                            <button class="message-bold" @click="getName(message)">
                                {{ message['msg'] }}
                            </button>
                        </template>
                        <template v-else>
                            <button class="message" @click="getName(message)">
                                {{ message['msg'] }}
                            </button>
                        </template>
                        <Dropdown-menu id="show" slot="list">
                            <Dropdown-item name="gag">禁言</Dropdown-item>
                            <Dropdown-item name="gagAll">全局禁言</Dropdown-item>
                            <Dropdown-item name="allowSpeak">单人解禁</Dropdown-item>
                            <Dropdown-item name="allowAllSpeak">全局解禁</Dropdown-item>
                            <Dropdown-item name="kickOut">踢出房间</Dropdown-item>
                        </Dropdown-menu>
                    </Dropdown>
                </div>
            </div>
            <Input v-model="msgInput" id="input">
            <Button id="send-btn" @click="sendMsg" slot="append">发送</Button>
            </Input>
            <Modal v-model="showGagList" title="解除禁言" @on-ok="allowSpeak">
                <label>请选择您要解除禁言的对象</label>
                <br>
                <br>
                <Checkbox-group v-model="speakList">
                    <Checkbox v-for="user in gagList" :label="user">{{ user }}</Checkbox>
                </Checkbox-group>
            </Modal>
        </div>
    </Card>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
/**
 * 实现聊天室功能，
 * 作为子组件插入直播间页面。
 *
 * @module ChatBoard
 * @class ChatBoard
 */
import * as io from 'socket.io-client'
import myMsg from './../warning.js'
export default {
    name: 'chat-board',
    props: ['roomId', 'teacherName', 'username', 'containerHeight'],
    data: function () {
        return {
            /**
             * 表示是否显示要禁言学生列表
             *
             * @attribute showGagList
             * @type Boolean
             * @default false
             */
            showGagList: false,
            /**
             * 表示客户端，负责监听服务器传来的消息
             *
             * @attribute socket
             * @type Object
             * @default ''
             */
            socket: '',
            /**
             * 表示老师踢出或禁言操作时选中的用户
             *
             * @attribute chosenUser
             * @type
             * @default ''
             */
            chosenUser: '',
            /**
             * 表示要禁言的学生列表
             *
             * @attribute gagList
             * @type Array
             * @default []
             */
            gagList: [],
            /**
             * 表示聊天区域所有发过言的学生列表
             *
             * @attribute speakList
             * @type Array
             * @default []
             */
            speakList: [],
            /**
             * 存储发言记录
             *
             * @attribute messages
             * @type Array
             * @default []
             */
            messages: [],
            /**
             * 表示文本框中输入的文字
             *
             * @attribute msgInput
             * @type String
             * @default ''
             */
            msgInput: '',
            /**
             * 表示老师是否选择开始直播，
             * 在直播前，即started值为false时不能记性发言。
             *
             * @attribute started
             * @type Boolean
             * @default false
             */
            started: false
        }
    },
    /**
     * mounted函数，初始化相关数据，客户端负责监听服务器传来的消息。
     *
     * @method mounted
     */
    mounted: function () {
        let self = this
        document.oncontextmenu = self.contextMenu
        self.socket = io.connect('http://localhost:9000')
        self.socket.emit('join', self.roomId + '.1', self.roomId)
        self.kickOut()
        self.changeStuNum()
        self.socket.on('message', function (data) {
            self.messages.push({
                'msg': data['message'],
                'isTeacher': data['isTeacher'],
                'user': data['user']
            })
            let scroll = document.getElementById('messages')
            scroll.scrollTop = scroll.scrollHeight
        })
        self.socket.on('getStarted', function () {
            self.started = true
        })
        document.getElementById('chat-board').style.height = (this.containerHeight - 32) + 'px'
    },
    methods: {
        /**
         * 获取被选中的学生名字
         *
         * @method getName
         * @param message
         */
        getName: function (message) {
            this.chosenUser = message['user']
            if (this.teacherName !== this.username) {
                let show = document.getElementById('show')
                show.style.display = 'none'
            }
        },
        /**
         * 屏蔽浏览器右键
         *
         * @method contextMenu
         * @return false
         */
        contextMenu: function () {
            return false
        },
        /**
         * 接收到'changeNum'消息时，发送'stuNum'，
         * 改变学生数量
         *
         * @method changeStuNum
         */
        changeStuNum: function () {
            let self = this
            self.socket.on('changeNum', function (count) {
                self.$emit('stuNum', count)
            })
        },
        /**
         * 用户接收到'kickOut'消息时（被提出房间时），弹出警告框进行提示
         *
         * @method kickOut
         */
        kickOut: function () {
            let self = this
            self.socket.on('kickOut', function (userid) {
                if (self.username === userid) {
                    self.$Message.warning(myMsg.chatroom['getKickedOut'])
                    setTimeout(window.close, 3000)
                }
            })
        },
        /**
         * 发送小时时，首先判断该用户是否被禁言，
         * 若没有被禁言，向服务器发送'message'消息。
         *
         * @method sendMsg
         */
        sendMsg: function () {
            if (this.msgInput === '') {
                return
            }
            fetch('/checkGag/', {
                method: 'post',
                mode: 'cors',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'name': this.username,
                    'roomID': this.roomId
                })
            }).then((response) => response.json()).then((obj) => {
                if (obj.result && this.started) {
                    this.socket.emit('message', {
                        type: 'chatroom',
                        user: this.username,
                        message: this.username + ' : ' + this.msgInput,
                        isTeacher: this.username === this.teacherName
                    }, this.roomId + '.1')
                    this.msgInput = ''
                } else {
                    this.$Message.error(myMsg.chatroom['beGaged'])
                }
            })
        },
        /**
         * 将被选中的用户禁言
         *
         * @method gag
         */
        gag: function () {
            this.$Message.warning('您将禁言用户： ' + this.chosenUser)
            fetch('/gag/', {
                method: 'post',
                mode: 'cors',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'name': this.chosenUser,
                    'roomID': this.roomId
                })
            }).then((response) => response.json()).then((obj) => {
                this.gagList.push(this.chosenUser)
            })
        },
        /**
         * 全局禁言
         *
         * @method gagAll
         */
        gagAll: function () {
            this.$Message.warning(myMsg.chatroom['gagAll'])
            fetch('/gagAll/', {
                method: 'post',
                mode: 'cors',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ 'roomID': this.roomId })
            }).then((response) => response.json()).then((obj) => {
                this.gagList = []
                this.gagList = obj.gagList
            })
        },
        /**
         * 全局解禁
         *
         * @method allowAllSpeak
         */
        allowAllSpeak: function () {
            this.$Message.warning(myMsg.chatroom['allowAllSpeak'])
            fetch('/allowAllSpeak/', {
                method: 'post',
                mode: 'cors',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ 'roomID': this.roomId })
            }).then((response) => response.json()).then((obj) => {
                this.gagList = []
            })
        },
        /**
         * 将被选中的学生踢出房间
         *
         * @method kickSomeoneOut
         */
        kickSomeoneOut: function () {
            if (this.chosenUser !== this.teacherName) {
                this.$Message.warning('您将踢出用户： ' + this.chosenUser)
                fetch('/kickOut/', {
                    method: 'post',
                    mode: 'cors',
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json, text/plain, */*',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        'name': this.chosenUser,
                        'roomID': this.roomId
                    })
                }).then((response) => response.json()).then((obj) => {
                    this.socket.emit('kickOut', this.chosenUser, this.roomId + '.1')
                })
            } else {
                this.$Message.warning(myMsg.chatroom['cannotKickOut'])
            }
        },
        /**
         * 老师进行的一些操作
         *
         * @method teacherDoing
         * @param name
         */
        teacherDoing: function (name) {
            if (name === 'gag') {
                this.gag()
            }
            if (name === 'gagAll') {
                this.gagAll()
            }
            if (name === 'allowSpeak') {
                this.showGagList = true
            }
            if (name === 'allowAllSpeak') {
                this.allowAllSpeak()
            }
            if (name === 'kickOut') {
                this.kickSomeoneOut()
            }
        },
        /**
         * 更新学生列表
         *
         * @method getName
         */
        resetList: function () {
            for (let i = this.gagList.length - 1; i >= 0; i--) {
                let a = this.gagList[i]
                for (let j = this.speakList.length - 1; j >= 0; j--) {
                    let b = this.speakList[j]
                    if (a === b) {
                        this.gagList.splice(i, 1)
                        this.speakList.splice(j, 1)
                        break
                    }
                }
            }
        },
        /**
         * 给特定用户解禁
         *
         * @method allowSpeak
         */
        allowSpeak: function () {
            let gagWarning = '您将为该房间内的以下用户解禁：\n'
            for (let i = 0; i < this.speakList.length; i++) {
                gagWarning += (this.speakList[i] + '  ')
            }
            this.$Message.warning(gagWarning)
            fetch('/allowSpeak/', {
                method: 'post',
                mode: 'cors',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'roomID': this.roomId,
                    'student': this.speakList
                })
            }).then((response) => response.json()).then((obj) => {
                this.resetList()
            })
        }
    },
    watch: {
        containerHeight: function (newVal, oldVal) {
            document.getElementById('chat-board').style.height = (newVal - 44) + 'px'
        }
    }
}
</script>

<style scoped>
* {
    overflow: hidden;
}

#chatboard-card {
    height: 100%;
}

#chat-board {
    width: 90%;
    position: absolute;
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

#input {
    top: auto;
    position: absolute;
    bottom: 0;
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
    height: 87%;
}
</style>
