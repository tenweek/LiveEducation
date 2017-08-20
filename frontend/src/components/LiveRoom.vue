<template>
    <div id="bg">
        <div class="live-room">
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
                        <Button @click="startLive" type="primary" shape="circle" size="small">开始直播</Button>
                    </template>
                </div>
            </div>
            <div class="layout-header" id="teaching">
                <div id="left-container">
                    <keep-alive>
                        <component :is="this.leftComponent" :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username" :teaching-tools-width="this.whiteBoardWidth" :teaching-tools-height="this.whiteBoardHeight"></component>
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
                            <component :is="this.rightComponent" :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username" :teaching-tools-width="this.whiteBoardWidth" :teaching-tools-height="this.whiteBoardHeight"></component>
                        </keep-alive>
                    </div>
                    <div id="chatroom">
                        <chat-board v-on:stuNum="getNum" :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username" :above-hidden="this.hidden"></chat-board>
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
/**
 * 直播间页面
 *
 * @module LiveRoom
 * @class LiveRoom
 */
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
            /**
             * 房间ID
             *
             * @attribute roomId
             * @type Number
             * @default -1
             */
            roomId: -1,
            /**
             * 房间名称
             *
             * @attribute roomName
             * @type String
             * @default ''
             */
            roomName: '',
            /**
             * 老师名字
             *
             * @attribute teacherName
             * @type String
             * @default ''
             */
            teacherName: '',
            /**
             * 在线人数
             *
             * @attribute studentNum
             * @type String
             * @default ''
             */
            studentNum: '',
            /**
             * 用户名字
             *
             * @attribute username
             * @type String
             * @default ''
             */
            username: '',
            /**
             * 教学区域div的宽
             *
             * @attribute teachingWidth
             * @type Number
             * @default 100
             */
            teachingWidth: 100,
            /**
             * 教学区域div的高
             *
             * @attribute teachingHeight
             * @type Number
             * @default 100
             */
            teachingHeight: 100,
            /**
             * 白板区域div的宽
             *
             * @attribute whiteBoardWidth
             * @type Number
             * @default 100
             */
            whiteBoardWidth: 100,
            /**
             * 白板区域div的高
             *
             * @attribute whiteBoardHeight
             * @type Number
             * @default 100
             */
            whiteBoardHeight: 100,
            /**
             * 表示左边的子组件
             *
             * @attribute leftComponent
             * @type String
             * @default 'TeachingTools'
             */
            leftComponent: 'TeachingTools',
            /**
             * 表示右边的子组件
             *
             * @attribute rightComponent
             * @type String
             * @default 'VideoDisplay'
             */
            rightComponent: 'VideoDisplay',
            /**
             * 表示是否隐藏视频区域
             *
             * @attribute hidden
             * @type Boolean
             * @default false
             */
            hidden: false,
            /**
             * 表示客户端，监听服务器传来的消息
             *
             * @attribute socket
             * @type Object
             * @default ''
             */
            socket: ''
        }
    },
    /**
     * created函数，初始化相关数据，客户端发送'joinRoom'消息
     *
     * @method created
     */
    created: function () {
        this.roomId = this.$route.params.id
        this.socket = io.connect('http://localhost:9000')
        this.socket.emit('joinRoom', this.roomId)
        this.getRoomInfo()
        this.getUsername()
        window.setInterval(this.changeNum, 5000)
    },
    /**
     * mounted函数，初始化教学区域和白板区域的长和高，
     * 并监测窗口大小的改变，实时变化相应参数
     *
     * @method mounted
     */
    mounted: function () {
        let self = this
        self.teachingWidth = document.getElementById('teaching').clientWidth
        self.teachingHeight = document.getElementById('teaching').clientHeight
        self.whiteBoardWidth = self.teachingWidth * 0.68 - 77
        self.whiteBoardHeight = self.teachingHeight - 35
        window.onresize = function () {
            self.teachingWidth = document.getElementById('teaching').clientWidth
            self.teachingHeight = document.getElementById('teaching').clientHeight
            self.whiteBoardWidth = self.teachingWidth * 0.68 - 77
            self.whiteBoardHeight = self.teachingHeight - 35
        }
    },
    methods: {
        /**
         * 开始直播，发送'startLive'消息
         *
         * @method startLive
         */
        startLive: function () {
            this.socket.emit('startLive', this.roomId)
        },
        /**
         * 隐藏视频区域，改变相关div的大小
         *
         * @method hide
         */
        hide: function () {
            let rightContent = document.getElementById('right-up-container')
            rightContent.style.display = 'none'
            this.hidden = true
            document.getElementById('chatroom').style.marginTop = '0'
            document.getElementById('chatroom').style.height = '100%'
        },
        /**
         * 弹出右边窗口
         *
         * @method popUp
         */
        popUp: function () {
            let rightContent = document.getElementById('right-up-container')
            rightContent.style.display = 'block'
            this.hidden = false
            document.getElementById('chatroom').style.marginTop = '2%'
            document.getElementById('chatroom').style.height = '56%'
        },
        /**
         * 左右子组件交换位置
         *
         * @method swap
         */
        swap: function () {
            let tmp = this.leftComponent
            this.leftComponent = this.rightComponent
            this.rightComponent = tmp
        },
        /**
         * 更新学生数量
         *
         * @method changeNum
         */
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
        /**
         * 获取学生数量
         *
         * @method getNum
         */
        getNum: function (count) {
            this.studentNum = count
        },
        /**
         * 获取房间信息
         *
         * @method getRoomInfo
         */
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
        /**
         * 获取用户名称
         *
         * @method getUsername
         */
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

.live-room {
    background: #f5f7f9;
    position: relative;
    border-radius: 5px;
    overflow: hidden;
    width: 177vmin;
    height: 100vmin;
    margin-left: auto;
    margin-right: auto;
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

.information {
    margin: 0 auto;
}

.layout-header {
    width: 78%;
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
