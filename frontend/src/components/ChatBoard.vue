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
            <Input v-model="msgInput">
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
 * @module ChatRoom
 * @class ChatRoom
 */
import * as io from 'socket.io-client'
import myMsg from './../warning.js'
export default {
    name: 'chat-board',
    /**
     *表示房间ID号
     *
     * @property roomId
     * @type String
     */

    /**
     *表示创建该房间的老师名字
     *
     * @property teacherName
     * @type String
     */

    /**
     *表示进入该房间的用户名字
     *
     * @property username
     * @type String
     */

     /**
      * 当有新的发言时，显示新的发言，并隐藏最远的一条记录。
      *
     * @property aboveHidden
     * @type Boolean
      */
    props: ['roomId', 'teacherName', 'username', 'aboveHidden'],
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
             * 表示老师提出或禁言操作时选中的用户
             *
             * @attribute choosenUser
             * @type 
             * @default ''
             */
            choosenUser: '',
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
             * 存储所有的发言记录
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
                'isTeacher': data['isTeacher']
            })
            let scroll = document.getElementById('messages')
            scroll.scrollTop = scroll.scrollHeight
        })
        self.socket.on('getStarted', function () {
            self.started = true
        })
    },
    methods: {
        /**
         * 
         *
         * @method getName
         * @param message
         */
        getName: function (message) {
            this.choosenUser = message['user']
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
         * 完成改变学生数量的目的
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
         * 点击发送按钮时响应，将输入框中的文字发送
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
         * 
         *
         * @method gag
         */
        gag: function () {
            this.$Message.warning('您将禁言用户： ' + this.choosenUser)
            fetch('/gag/', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'name': this.choosenUser,
                    'roomID': this.roomId
                })
            }).then((response) => response.json()).then((obj) => {
                this.gagList.push(this.choosenUser)
            })
        },
        /**
         * 
         *
         * @method gagAll
         */
        gagAll: function () {
            this.$Message.warning(myMsg.chatroom['gagAll'])
            fetch('/gagAll/', {
                method: 'post',
                mode: 'cors',
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
         * 
         *
         * @method allowAllSpeak
         */
        allowAllSpeak: function () {
            this.$Message.warning(myMsg.chatroom['allowAllSpeak'])
            fetch('/allowAllSpeak/', {
                method: 'post',
                mode: 'cors',
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
         * 
         *
         * @method kickSomeoneOut
         */
        kickSomeoneOut: function () {
            if (this.choosenUser !== this.teacherName) {
                this.$Message.warning('您将踢出用户： ' + this.choosenUser)
                fetch('/kickOut/', {
                    method: 'post',
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json, text/plain, */*',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        'name': this.choosenUser,
                        'roomID': this.roomId
                    })
                }).then((response) => response.json()).then((obj) => {
                    this.socket.emit('kickOut', this.choosenUser, this.roomId + '.1')
                })
            } else {
                this.$Message.warning(myMsg.chatroom['cannotKickOut'])
            }
        },
        /**
         * 
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
         * 
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
         * 
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
        aboveHidden: function (newVal, oldVal) {
            if (newVal) {
                document.getElementById('messages').style.height = '90%'
                document.getElementById('chat-board').style.height = '76vmin'
            } else {
                document.getElementById('messages').style.height = '87%'
                document.getElementById('chat-board').style.height = '40vmin'
            }
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
    width: 100%;
    height: 40vmin;
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
    height: 87%;
}
</style>
