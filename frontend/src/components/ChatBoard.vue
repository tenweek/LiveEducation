<template>
    <div class="chat-board">
        <div v-for="message in messages">
            <Dropdown class="set-left" trigger="click" @on-click="teacherDoing">
                <button class="message" @click="getName(message)">
                    {{ message }}
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
        <form>
            <img src="../assets/chat_bottombar_icon_face.png">
            <input id="msgInput" class="msg-input" autocomplete="off" />
            <button @click="sendMsg">Send</button>
        </form>
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
export default {
    name: 'chat-board',
    props: ['id', 'teacherName', 'username'],
    data: function () {
        return {
            showGagList: false,
            socket: '',
            choosenUser: '',
            gagList: [],
            speakList: [],
            messages: []
        }
    },
    mounted: function () {
        let self = this
        document.oncontextmenu = self.contextMenu
        self.socket = io.connect('http://localhost:9000')
        self.socket.emit('join', self.id + '.1')
        if (self.teacherName === self.username) {
            self.changeStuNum()
        } else {
            self.kickOut()
        }
        self.socket.on('message', function (data) {
            self.messages.push(data['username'] + ' : ' + data['message'])
        })
    },
    methods: {
        getName: function (message) {
            this.choosenUser = message.split(':')[0].replace(/(^\s*)|(\s*$)/g, '')
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
                    this.$Message.warning('您将在 ' + 3 + ' 秒后被踢出直播间')
                    setTimeout(window.close, 3000)
                }
            })
        },
        sendMsg: function () {
            let msg = document.getElementById('msgInput').value
            if (msg === '') {
                return
            }
            document.getElementById('msgInput').value = ''
            fetch('/checkGag/', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'name': this.username,
                    'roomID': this.id
                })
            }).then((response) => response.json()).then((obj) => {
                if (obj.result) {
                    this.socket.emit('message', { message: msg, username: this.username }, this.id + '.1')
                } else {
                    this.$Message.error('您已被禁言')
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
                    'roomID': this.id
                })
            }).then((response) => response.json()).then((obj) => {
                this.gagList.push(this.choosenUser)
            })
        },
        gagAll: function () {
            this.$Message.warning('您将禁言该房间内的所有用户')
            fetch('/gagAll/', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ 'roomID': this.id })
            }).then((response) => response.json()).then((obj) => {
                this.gagList = []
                this.gagList = obj.gagList
            })
        },
        allowAllSpeak: function () {
            this.$Message.success('您将为该房间内的所有用户解禁')
            fetch('/allowAllSpeak/', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ 'roomID': this.id })
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
                        'roomID': this.id
                    })
                }).then((response) => response.json()).then((obj) => {
                    this.socket.emit('kickOut', this.choosenUser, this.id + '.1')
                })
            } else {
                this.$Message.warning('您不可踢出自己')
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
            let s = '您将为该房间内的以下用户解禁：\n'
            for (let i = 0; i < this.speakList.length; i++) {
                s += (this.speakList[i] + '  ')
            }
            this.$Message.success(s)
            fetch('/allowSpeak/', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'roomID': this.id,
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

form img {
    margin-bottom: -10px;
    height: 30px;
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

#msg-input {
    width: 292px;
}
</style>
