<template>
    <div class="chat-board">
        <div id="messages">
            <div v-for="message in messages">
                <Dropdown class="set-left" trigger="click" @on-click="teacherDoing">
                    <button class="message" @click="getName(message)">
                        {{ message['msg'] }}
                    </button>
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
        <Form class="form" inline>
            <Form-item class="item-img">
                <img class="img" src="../assets/chat_bottombar_icon_face.png">
            </Form-item>
            <Form-item class="item-input">
                <Input v-model="msgInput"></Input>
            </Form-item>
            <Form-item class="item-button">
                <Button type="ghost" class="button" @click="sendMsg">发送</Button>
            </Form-item>
        </Form>
        <Modal v-model="showGagList" title="解除禁言" @on-ok="allowSpeak">
            <label>请选择您要解除禁言的对象</label>
            <br>
            <br>
            <Checkbox-group v-model="speakList">
                <Checkbox v-for="user in gagList" :label="user">{{ user }}</Checkbox>
            </Checkbox-group>
        </Modal>
    </div>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
import * as io from 'socket.io-client'
import myMsg from './../warning.js'
export default {
    name: 'chat-board',
    props: ['roomId', 'teacherName', 'username'],
    data: function () {
        return {
            showGagList: false,
            socket: '',
            choosenUser: '',
            gagList: [],
            speakList: [],
            messages: [],
            msgInput: ''
        }
    },
    mounted: function () {
        let self = this
        document.oncontextmenu = self.contextMenu
        self.socket = io.connect('http://localhost:9000')
        self.socket.emit('join', self.id + '.1')
        self.kickOut()
        self.socket.on('message', function (data) {
            let msg = data['username'] + ' : ' + data['message']
            self.messages.push({ 'msg': msg, 'user': data['username'] })
            let scroll = document.getElementById('messages')
            scroll.scrollTop = scroll.scrollHeight
        })
    },
    methods: {
        getName: function (message) {
            this.choosenUser = message['user']
            if (this.teacherName !== this.username) {
                let show = document.getElementById('show')
                show.style.display = 'none'
            }
        },
        contextMenu: function () {
            return false
        },
        changeStuNum: function () {
            // 这个地方更新在线人数
            this.socket.on('login', function (count) {
                console.log(count)
            })
            this.socket.on('logout', function (count) {
                console.log(count)
            })
        },
        kickOut: function () {
            this.socket.on('kickOut', function (userid) {
                if (this.username === userid) {
                    this.$Message.warning(myMsg.chatroom['getKickedOut'])
                    setTimeout(window.close, 3000)
                }
            })
        },
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
                if (obj.result) {
                    this.socket.emit('message', { message: this.msgInput, username: this.username }, this.roomId + '.1')
                    this.msgInput = ''
                } else {
                    this.$Message.error(myMsg.chatroom['beGaged'])
                }
            })
        },
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
    }
}
</script>

<style scoped>
* {
    overflow: hidden;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.chat-board {
    width: 100%;
    height: 100%;
    position: relative;
}

.message {
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

.set-left {
    float: left;
    padding-left: 5px;
}

.form {
    height: 38px;
    width: 100%;
    position: absolute;
    bottom: 0px;
}

.chat-board .form .item-button,
.chat-board .form .item-img,
.chat-board .form .item-input {
    margin-top: 6px;
    margin-bottom: 0px;
    margin-right: 0px;
}

.item-img {
    width: 9.1%;
}

.item-input {
    width: 68.1%;
}

.item-button {
    width: 20%;
}

.img {
    height: 30px;
    width: 30px;
}

.button {
    color: white;
    background-color: #1EE494;
}

#messages {
    overflow: auto;
    height: 91%;
}
</style>