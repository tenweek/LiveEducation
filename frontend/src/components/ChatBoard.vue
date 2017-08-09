<template>
    <div class="chat-board">
        <ul id="messages"></ul>
        <form action="">
            <img src="../assets/chat_bottombar_icon_face.png">
            <input id="msgInput" class="msgInput" autocomplete="off" />
            <button @click="sendMsg">Send</button>
        </form>
        <Menu id="menu" mode="horizontal" :theme="theme1" active-name="1" style='display:none'>
            <Submenu name="3">
                <template slot="title">
                    <Icon type="stats-bars"></Icon>
                    统计分析
                </template>
                <Menu-group title="使用">
                    <Menu-item name="3-1">新增和启动</Menu-item>
                    <Menu-item name="3-2">活跃分析</Menu-item>
                    <Menu-item name="3-3">时段分析</Menu-item>
                </Menu-group>
                <Menu-group title="留存">
                    <Menu-item name="3-4">用户留存</Menu-item>
                    <Menu-item name="3-5">流失用户</Menu-item>
                </Menu-group>
            </Submenu>
        </Menu>
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
            socket: '',
            username: ''
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
            fetch('getName', {
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
        // 监听
        this.socket = io.connect('http://localhost:9000')
        this.socket.emit('join', this.id + '.1')
        this.socket.on('message', function (data) {
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
            // 如果判定是本人就给字体加粗 判断未生效
            if (data.username === this.username) {
                style += 'font-weight:bold;'
            }
            button.style = style
            button.onmousedown = function (oEvent) {
                let memu = document.getElementById('menu')
                alert('ss')
                // memu.style.display = 'block'
                // memu.style.position = 'absolute'
                // memu.style.left = oEvent.pageY
                // memu.style.top = oEvent.pageX
                memu.style = ('display:block;position:absolute;left:' + oEvent.pageX + ';top:' + oEvent.pageY + ';')
                // // 如果是老师就有操作权限 判断未生效
                // if (this.teacherName === this.username) {
                //     if (!oEvent) {
                //         oEvent = window.event
                //     }
                //     if (oEvent.button === 2) {
                //         alert('您将禁言用户： ' + data['username'])
                //         fetch('gag', {
                //             method: 'post',
                //             mode: 'cors',
                //             headers: {
                //                 'Content-Type': 'application/json, text/plain, */*',
                //                 'Accept': 'application/json'
                //             },
                //             body: JSON.stringify({
                //                 'name': data['username'],
                //                 'roomID': this.id
                //             })
                //         }).then((response) => response.json()).then((obj) => { })
                //     }
                // }
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
            fetch('checkGag', {
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
