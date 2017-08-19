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
                        <Button type="error" shape="circle" size="small" id="stop-live-button">结束直播</Button>
                    </template>
                </div>
            </div>
            <div class="layout-header">
                <div id="left-container">
                    <keep-alive>
                        <component :is="this.leftComponent" :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username" :container-height="this.leftContainerHeight" :container-width="this.leftContainerWidth"></component>
                    </keep-alive>
                </div>
                <div id="buttons-panel">
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
                            <Button id="hide-button" type="ghost" @click="hide">
                                <Icon type="ios-undo"></Icon>
                            </Button>
                        </Tooltip>
                    </template>
                </div>
                <div id="right-container">
                    <div id="right-up-container">
                        <keep-alive>
                            <component :is="this.rightComponent" :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username" :container-height="this.rightUpContainerHeight" :container-width="this.rightUpContainerWidth"></component>
                        </keep-alive>
                    </div>
                    <div id="chatroom">
                        <chat-board v-on:stuNum="getNum" :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username" :above-is-hidden="this.hidden"></chat-board>
                    </div>
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
            leftComponent: 'TeachingTools',
            rightComponent: 'VideoDisplay',
            hidden: false,
            socket: '',
            leftContainerHeight: 0,
            leftContainerWidth: 0,
            rightUpContainerHeight: 0,
            rightUpContainerWidth: 0
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
        let unit = Math.min(window.innerWidth / 1.33, window.innerHeight)
        document.getElementById('live-room').style.width = (1.33 * unit) + 'px'
        document.getElementById('live-room').style.height = unit + 'px'
        self.leftContainerWidth = (1.33 * unit * 0.9 * 0.68)
        self.leftContainerHeight = (0.78 * unit)
        self.rightUpContainerWidth = (1.33 * unit * 0.9 * 0.3)
        self.rightUpContainerHeight = (0.78 * unit * 0.3)
        window.onresize = function () {
            let unit = Math.min(window.innerWidth / 1.33, window.innerHeight)
            document.getElementById('live-room').style.width = (1.33 * unit) + 'px'
            document.getElementById('live-room').style.height = unit + 'px'
            self.leftContainerWidth = (1.33 * unit * 0.9 * 0.68)
            self.leftContainerHeight = (0.78 * unit)
            self.rightUpContainerWidth = (1.33 * unit * 0.9 * 0.3)
            self.rightUpContainerHeight = (0.78 * unit * 0.3)
        }
    },
    methods: {
        startLive: function () {
            this.socket.emit('startLive', this.roomId)
            document.getElementById('start-live-button').style.display = 'none'
            document.getElementById('stop-live-button').style.display = 'inline-block'
        },
        hide: function () {
            let rightContent = document.getElementById('right-up-container')
            rightContent.style.display = 'none'
            this.hidden = true
            document.getElementById('chatroom').style.marginTop = '0'
            document.getElementById('chatroom').style.height = '100%'
        },
        popUp: function () {
            let rightContent = document.getElementById('right-up-container')
            rightContent.style.display = 'block'
            this.hidden = false
            document.getElementById('chatroom').style.marginTop = '2%'
            document.getElementById('chatroom').style.height = '56%'
        },
        swap: function () {
            let tmp = this.leftComponent
            this.leftComponent = this.rightComponent
            this.rightComponent = tmp
        },
        changeNum: function () {
            if (this.username === this.teacherName) {
                fetch('/changeNum/', {
                    method: 'post',
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json, text/plain, */*',
                        'Accept': 'application/json'
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

#left-container {
    height: 100%;
    width: 68%;
    text-align: left;
    overflow: hidden;
}

#right-container {
    width: 30%;
    height: 100%;
}

#right-up-container {
    width: 100%;
}

#chatroom {
    margin-top: 2%;
    height: 56%;
    width: 100%;
}

#swap-button,
#pop-up-button,
#hide-button {
    height: 41px;
    border: none;
}
</style>
