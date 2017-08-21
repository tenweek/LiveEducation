<template>
    <div id="bg">
        <div id="live-room">
            <div class="header">
                <home-page-header></home-page-header>
            </div>
            <div class="navigation">
                <div class="welcome">
                    <Icon type="university"></Icon>
                    <label>欢迎进入直播间 !</label>
                </div>
                <div class="navigation-center">
                    <label class="information">老师姓名：{{ this.teacherName }}</label>
                    <label class="information">房间ID:{{ this.roomId }}</label>
                    <label class="information">房间名：{{ this.roomName }}</label>
                    <label class="information">在线人数：{{ this.studentNum }}</label>
                </div>
                <div class="navigation-right">
                    <template v-if="this.teacherName === this.username">
                        <Button @click="startLive" type="primary" shape="circle" size="small" id="start-live-button">开始直播</Button>
                        <Button @click="closeLive" type="error" shape="circle" size="small" id="stop-live-button">结束直播</Button>
                    </template>
                </div>
            </div>
            <div class="layout-header">
                <div class="left-container" id="teaching-tools">
                    <teaching-tools :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username" :container-height="this.teachingToolsHeight" :container-width="this.teachingToolsWidth" :tools-on-left="this.toolsOnLeft"></teaching-tools>
                </div>
                <div class="buttons-panel">
                    <template v-if="this.hidden === true">
                        <Tooltip content="弹出右边窗口" placement="right-start">
                            <Button id="pop-up-button" type="ghost" @click="popUp">
                                <Icon type="ios-redo"></Icon>
                            </Button>
                        </Tooltip>
                    </template>
                    <template v-else>
                        <Tooltip content="切换位置" placement="right-start">
                            <Button id="swap-button" type="ghost" @click="swap">
                                <Icon type="arrow-swap"></Icon>
                            </Button>
                        </Tooltip><br>
                        <Tooltip content="隐藏右边窗口" placement="right-start">
                            <Button id="hide-button" type="ghost" @click="hideRight">
                                <Icon type="ios-undo"></Icon>
                            </Button>
                        </Tooltip><br>
                        <Tooltip content="隐藏左边窗口" placement="right-start">
                            <Button id="hide-button" type="ghost" @click="hideLeft">
                                <Icon type="ios-redo"></Icon>
                            </Button>
                        </Tooltip>
                    </template>
                </div>
                <div class="right-up-container" id="video-display">
                    <video-display :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username" :container-height="this.videoDisplayHeight"></video-display>
                </div>
                <div id="chatroom">
                    <chat-board v-on:stuNum="getNum" :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username" :container-height="this.chatBoardHeight" ></chat-board>
                </div>
            </div>
            <div>
                <page-footer></page-footer>
            </div>
        </div>
    </div>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
import * as io from 'socket.io-client'
import myMsg from './../warning.js'
import HomePageHeader from './HomePageHeader'
import PageFooter from './PageFooter'
import VideoDisplay from './VideoDisplay'
import ChatBoard from './ChatBoard'
import TeachingTools from './TeachingTools'

export default {
    name: 'live-room',
    components: {
        HomePageHeader,
        PageFooter,
        ChatBoard,
        VideoDisplay,
        TeachingTools
    },
    data: function () {
        return {
            roomId: -1,
            roomName: '',
            teacherName: '',
            studentNum: '',
            username: '',
            hidden: false,
            socket: '',
            startTime: '',
            toolsOnLeft: true,
            teachingToolsHeight: 0,
            teachingToolsWidth: 0,
            videoDisplayHeight: 0,
            chatBoardHeight: 0
        }
    },
    created: function () {
        this.roomId = this.$route.params.id
        this.socket = io.connect('http://localhost:9000')
        this.socket.emit('joinRoom', this.roomId)
        this.getRoomInfo()
        this.getUsername()
        window.setInterval(this.changeNum, 5000)
    },
    mounted: function () {
        let self = this
        document.getElementById('bg').style.height = window.innerHeight + 'px'
        document.getElementById('bg').style.width = window.innerWidth + 'px'
        let unit = Math.min(window.innerWidth / 1.33, window.innerHeight)
        document.getElementById('live-room').style.width = (1.33 * unit) + 'px'
        document.getElementById('live-room').style.height = unit + 'px'
        self.teachingToolsWidth = document.getElementById('teaching-tools').clientWidth
        self.teachingToolsHeight = document.getElementById('teaching-tools').clientHeight
        self.videoDisplayHeight = document.getElementById('video-display').clientHeight
        self.chatBoardHeight = document.getElementById('chatroom').clientHeight
        window.onresize = function () {
            document.getElementById('bg').style.height = window.innerHeight + 'px'
            document.getElementById('bg').style.width = window.innerWidth + 'px'
            let unit = Math.min(window.innerWidth / 1.33, window.innerHeight)
            document.getElementById('live-room').style.width = (1.33 * unit) + 'px'
            document.getElementById('live-room').style.height = unit + 'px'
            self.teachingToolsWidth = document.getElementById('teaching-tools').clientWidth
            self.teachingToolsHeight = document.getElementById('teaching-tools').clientHeight
            self.videoDisplayHeight = document.getElementById('video-display').clientHeight
            self.chatBoardHeight = document.getElementById('chatroom').clientHeight
        }
        self.socket.on('closeLive', function () {
            self.$Message.warning(myMsg.room['endLive'])
            setTimeout(window.close, 3000)
        })
        self.socket.on('time', function (time) {
            self.startTime = time
            fetch('/startRecord/', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'channel': self.roomId,
                    'time': self.startTime
                })
            }).then((response) => response.json()).then((obj) => { })
        })
    },
    methods: {
        closeLive: function () {
            this.socket.emit('closeLive', this.roomId)
            fetch('/closeLiveRoom/', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'roomId': this.roomId
                })
            }).then((response) => response.json()).then((obj) => { })
        },
        startLive: function () {
            this.socket.emit('startLive', this.roomId)
            document.getElementById('start-live-button').style.display = 'none'
            document.getElementById('stop-live-button').style.display = 'inline-block'
        },
        hideLeft: function () {
            this.swap()
            this.hideRight()
        },
        hideRight: function () {
            document.getElementsByClassName('right-up-container')[0].style.display = 'none'
            this.hidden = true
            document.getElementById('chatroom').style.paddingTop = '0'
            document.getElementById('chatroom').style.height = '78%'
            document.getElementById('chatroom').style.top = 'inherit'
            this.chatBoardHeight = document.getElementById('chatroom').clientHeight
        },
        popUp: function () {
            document.getElementsByClassName('right-up-container')[0].style.display = 'block'
            this.hidden = false
            document.getElementById('chatroom').style.paddingTop = '12px'
            document.getElementById('chatroom').style.height = '52.5%'
            document.getElementById('chatroom').style.top = '42%'
            this.chatBoardHeight = document.getElementById('chatroom').clientHeight
        },
        swap: function () {
            let teachingTools = document.getElementById('teaching-tools')
            teachingTools.className = teachingTools.className === 'left-container' ? 'right-up-container' : 'left-container'
            let videoDisplay = document.getElementById('video-display')
            videoDisplay.className = videoDisplay.className === 'left-container' ? 'right-up-container' : 'left-container'
            this.toolsOnLeft = !this.toolsOnLeft
            this.teachingToolsWidth = document.getElementById('teaching-tools').clientWidth
            this.teachingToolsHeight = document.getElementById('teaching-tools').clientHeight
            this.videoDisplayWidth = document.getElementById('video-display').clientWidth
            this.videoDisplayHeight = document.getElementById('video-display').clientHeight
        },
        changeNum: function () {
            if (this.username === this.teacherName) {
                fetch('/changeNum/', {
                    method: 'post',
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json, text/plain, */*',
                        'Accept': 'applica tion/json'
                    },
                    body: JSON.stringify({
                        'studentNum': this.studentNum,
                        'roomId': this.roomId
                    })
                }).then((response) => response.json()).then((obj) => { })
            }
        },
        getNum: function (count) {
            this.studentNum = count
        },
        getRoomInfo: function () {
            fetch('/getRoomInfo/', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'roomID': this.roomId
                })
            }).then((response) => response.json()).then((obj) => {
                this.roomName = obj.roomName
                this.studentNum = obj.stuNum
                this.teacherName = obj.teacherName
            })
        },
        getUsername: function () {
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
        }
    }
}
</script>

<style scoped>
#bg {
    background: #f5f7f9;
    min-height: 600px;
    min-width: 800px;
}

#live-room {
    background: #f5f7f9;
    position: relative;
    border-radius: 5px;
    overflow: hidden;
    width: 177vmin;
    height: 100vmin;
    margin-left: auto;
    margin-right: auto;
    min-height: 600px;
    min-width: 800px;
}

.header {
    height: 60px;
    width: 100%;
    font-size: 40px;
    position: fixed;
    left: 0;
    z-index: 50;
}

.navigation {
    background: #efefef;
    padding: 8px 10px;
    overflow: hidden;
    display: flex;
    position: fixed;
    left: 0;
    top: 60px;
    width: 100%;
    font-size: 15px;
}

.navigation-center {
    margin: 0 auto;
    font-size: 15px;
}

.navigation-right {
    margin-right: 15px;
    width: 64px;
    font-size: 15px;
}

#stop-live-button {
    display: none;
}

.information {
    margin: 0 auto;
}

.layout-header {
    width: 90%;
    height: 78%;
    min-width: 800px;
    display: flex;
    margin-left: auto;
    margin-right: auto;
    margin-top: 110px;
}

.left-container {
    position: absolute;
    left: 0;
    height: 78%;
    width: 67%;
    text-align: left;
    overflow: hidden;
}

.right-up-container {
    display: block;
    height: 27%;
    position: absolute;
    left: 70%;
    width: 30%
}

#chatroom {
    position: absolute;
    left: 70%;
    top: 42%;
    padding-top: 12px;
    height: 52.5%;
    width: 30%;
}

.buttons-panel {
    position: absolute;
    left: 66.4%;
}

#swap-button,
#pop-up-button,
#hide-button {
    height: 41px;
    border: none;
}
</style>
