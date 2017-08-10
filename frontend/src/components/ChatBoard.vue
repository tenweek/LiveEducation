<template>
    <div class="chat-board">
        <ul id="messages"></ul>
        <form action="">
            <img src="../assets/chat_bottombar_icon_face.png">
            <input id="msgInput" class="msgInput" autocomplete="off" />
            <button @click="sendMsg">Send</button>
        </form>
        <Dropdown trigger="click" @on-click="teacherDoing">
            <label id="menu"></label>
            <Dropdown-menu id="show" slot="list">
                <Dropdown-item name="gag">禁言</Dropdown-item>
                <Dropdown-item name="gagAll">全局禁言</Dropdown-item>
                <Dropdown-item name="allowSpeak">单人解禁</Dropdown-item>
                <Dropdown-item name="allowAllSpeak">全局解禁</Dropdown-item>
                <Dropdown-item name="kickOut">踢出房间</Dropdown-item>
            </Dropdown-menu>
        </Dropdown>
        <Modal v-model="showGagList" title="解除禁言" @on-ok="allowSpeak">
            <label id="new-username">请选择您要接触禁言的对象</label><br><br>
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
    props: ['id', 'teacherName'],
    data: function () {
        return {
            showGagList: false,
            socket: '',
            username: '',
            choosenUser: '',
            gagList: [],
            speakList: []
        }
    },
    created: function () {
        let arrCookies = document.cookie.split(';')
        let account = ''
        for (let i = 0; i < arrCookies.length; i++) {
            let arrStr = arrCookies[i].split('=')
            if (arrStr[0].replace(/(^\s*)|(\s*$)/g, '') === 'userAccount') {
                account = arrStr[1].replace(/(^\s*)|(\s*$)/g, '')
            }
        }
        if (account !== '') {
            fetch('/getName/', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ 'account': account })
            }).then((response) => response.json()).then((obj) => {
                this.username = obj.name
            })
        }
    },
    mounted: function () {
        // 监听
        let self = this
        self.socket = io.connect('http://localhost:9000')
        self.socket.emit('join', self.id + '.1')
        self.socket.on('message', function (data) {
            let ul = document.getElementById('messages')
            let li = document.createElement('li')
            // 创建button
            let button = document.createElement('input')
            button.type = 'button'
            button.value = data['username'] + ' : ' + data['message']
            let styleArr = ['background-color:Transparent;', 'border-style:None;', 'outline:none;',
                'word-wrap: break-word !important;', 'word-break: break-all !important;',
                'white-space: normal !important;', 'text-align:left;', 'padding-left:10px;',
                'float:left;', 'padding-left:0px;', 'width:100%;']
            let style = ''
            for (let i = 0; i < styleArr.length; i++) {
                style += styleArr[i]
            }
            // 如果判定是本人就给字体加粗
            if (data['username'] === self.username) {
                style += 'font-weight:bold;'
            }
            button.style = style
            button.onmousedown = function (oEvent) {
                // 如果是老师就有操作权限
                if (self.teacherName === self.username) {
                    if (!oEvent) {
                        oEvent = window.event
                    }
                    // 如果是右键则出现
                    if (oEvent.button === 2) {
                        let menu = document.getElementById('menu')
                        menu.click()
                        let show = document.getElementById('show')
                        let left = oEvent.pageX - 500
                        let top = oEvent.pageY - 588
                        show.style = ('position:absolute;left:' + left + 'px;top:' + top + 'px;')
                        self.choosenUser = data['username']
                    }
                }
            }
            // 屏蔽右键菜单
            button.oncontextmenu = function () {
                return false
            }
            li.appendChild(button)
            ul.insertBefore(li, ul.childNodes[ul.childNodes.length])
            ul.scrollTop = ul.scrollHeight
        })
    },
    methods: {
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
        teacherDoing: function (name) {
            if (name === 'gag') {
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
            }
            if (name === 'gagAll') {
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
            }
            if (name === 'allowSpeak') {
                this.showGagList = true
            }
            if (name === 'allowAllSpeak') {
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
            }
            if (name === 'kickOut') {
                alert('滚蛋')
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
                // this.gagList = []
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

#msgInput {
    width: 292px;
}
</style>
