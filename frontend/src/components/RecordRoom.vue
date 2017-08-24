<template>
    <div id="bg">
        <div id="record-room">
            <div class="header">
                <home-page-header></home-page-header>
            </div>
            <div class="navigation">
                <div class="navigation-content">
                    <div class="welcome">
                        <Icon type="university"></Icon>
                        <label>欢迎进入录播间 !</label>
                    </div>
                     <div class="navigation-center">
                        <label class="information">老师姓名：{{ this.userAccount }}</label>
                        <label class="information">房间ID:{{ this.roomId }}</label>
                        <label class="information">房间名：{{ this.roomName }}</label>
                    </div>
                     <div class="navigation-right">
                        <template v-if="this.teacherName === this.username">
                            <Button @click="start" type="primary" shape="circle" size="small" id="start-button">开始播放</Button>
                            <Button @click="pause" type="error" shape="circle" size="small" id="pause-button">暂停播放</Button>
                        </template>
                    </div>
                </div>
            </div>
            <div class="layout-header">
                <div class="teaching-tools" id="teaching-tools">
                    <Card dis-hover>
                        <div class="choose-current">
                            <Button type="ghost">
                                教学区
                            </Button>
                        </div>
                        <keep-alive>
                            <component :is="currentTools" :userAccount="this.userAccount" :roomId="this.roomId" :teaching-tools-width="this.teachingToolsWidth" :teaching-tools-height="this.teachingToolsHeight"></component>
                        </keep-alive>
                    </Card>
                </div>
                <div class="video-live" id="video-live">
                    <Card dis-hover>
                        <video :src=videoPath id="video" :width="this.videoWidth" :height="this.videoHeight"></video>
                    </Card>
                </div>
                <div class="chatroom" id="chatroom">
                    <Card dis-hover>
                        <chat-board-for-record :roomId="this.roomId" :userAccount="this.userAccount" :chat-board-height="this.chatBoardHeight"></chat-board-for-record>
                    </Card>
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
 * 录播间页面，实现教学区、视频区及聊天室的复现，
 * 有暂停功能。
 *
 * @module RecordRoom
 * @class RecordRoom
 */
import HomePageHeader from './HomePageHeader'
import PageFooter from './PageFooter'
import ChatBoardForRecord from './ChatBoardForRecord'
import FileDisplayForRecord from './FileDisplayForRecord'
import WhiteBoardForRecord from './WhiteBoardForRecord'
import CodeEditorForRecord from './CodeEditorForRecord'
import * as io from 'socket.io-client'

export default {
    name: 'record-room',
    components: {
        HomePageHeader,
        PageFooter,
        ChatBoardForRecord,
        FileDisplayForRecord,
        WhiteBoardForRecord,
        CodeEditorForRecord
    },
    data: function () {
        return {
            /**
             * 表示当前选择的工具（白板、PPT、代码编辑器）
             *
             * @attribute currentTools
             * @type String
             * @default 'WhiteBoardForRecord'
             */
            currentTools: 'WhiteBoardForRecord',
            /**
             * 表示房间ID信息
             *
             * @attribute roomId
             * @type String
             * @default ''
             */
            roomId: '',
            /**
             * 房间的视频文件路径
             *
             * @attribute videoPath
             * @type String
             * @default ''
             */
            videoPath: '',
            /**
             * 表示用户账号信息
             *
             * @attribute userAccount
             * @type String
             * @default ''
             */
            userAccount: '',
            teachingToolsHeight: 0,
            teachingToolsWidth: 0,
            videoWidth: 0,
            videoHeight: 0,
            chatBoardHeight: 0,
            play: false
        }
    },
    /**
     * created函数
     *
     * @method mounted
     */
    created: function () {
        this.roomId = this.$route.params.id
        fetch('/getName/', {
            method: 'post',
            mode: 'cors',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json, text/plain, */*',
                'Accept': 'application/json'
            },
            body: JSON.stringify({})
        }).then((response) => response.json()).then((obj) => {
            if (obj.result) {
                this.userAccount = obj.account
            } else {
                this.$router.push({ name: 'home' })
            }
        })
    },
    /**
     * mounted函数，当接收到'changeCurrent'消息时改变相应属性值
     *
     * @method mounted
     */
    mounted: function () {
        let self = this
        self.videoPath = './../../static/record/' + self.roomId + '.mp4'
        self.socket = io.connect('http://localhost:9000')
        self.socket.emit('joinTest', self.roomId, 'tools')
        self.socket.on('changeCurrent', function (data) {
            self.currentTools = data['name'] + 'ForRecord'
        })
        self.resize(self)
        window.onresize = () => {
            let self = this
            this.resize(self)
        }
    },
    methods: {
        resize: function (self) {
            document.getElementById('bg').style.height = window.innerHeight + 'px'
            document.getElementById('bg').style.width = window.innerWidth + 'px'
            self.teachingToolsWidth = document.getElementById('teaching-tools').clientWidth - 32
            self.teachingToolsHeight = document.getElementById('teaching-tools').clientHeight - 64
            self.videoWidth = document.getElementById('video-live').clientWidth - 32
            self.videoHeight = document.getElementById('video-live').clientHeight - 32
            self.chatBoardHeight = document.getElementById('chatroom').clientHeight - 44
        },
        start: function () {
            document.getElementById('start-button').style.display = 'none'
            document.getElementById('pause-button').style.display = 'inline-block'
            this.play = true
            this.socket.emit('pause')
        },
        pause: function () {
            document.getElementById('pause-button').style.display = 'none'
            document.getElementById('start-button').style.display = 'inline-block'
            this.play = false
            this.socket.emit('pause')
        }
    },
    watch: {
        play: function (newVal, oldVal) {
            if (newVal === true) {
                document.getElementById('video').play()
            } else {
                document.getElementById('video').pause()
            }
        }
    }
}
</script>

<style scoped>
#bg {
    min-width: 800px;
    min-height: 600px;
}

#record-room {
    background: transparent;
    position: relative;
    border-radius: 5px;
    overflow: hidden;
    width: 85%;
    height: 100%;
    margin-left: auto;
    margin-right: auto;
    min-height: 600px;
    min-width: 800px;
    max-width: 1200px;
}

.header {
    height: 50px;
    width: 100%;
    font-size: 40px;
    position: fixed;
    left: 0;
    z-index: 50;
}

.navigation {
    background-color: rgba(239, 239, 239, 0.6);
    padding: 8px 10px;
    overflow: hidden;
    display: flex;
    position: fixed;
    left: 0;
    top: 50px;
    width: 100%;
    font-size: 15px;
}

.navigation-content {
    width: 85%;
    min-width: 800px;
    max-width: 1200px;
    display: flex;
    margin: auto;
}

.navigation-center {
    margin: 0 auto;
    font-size: 15px;
}

.navigation-right {
    width: 79px;
    font-size: 15px;
}

#pause-button {
    display: none;
}

.information {
    margin: 0 auto;
}

.layout-header {
    width: 100%;
    height: 78%;
    min-width: 800px;
    display: flex;
    margin-left: auto;
    margin-right: auto;
    margin-top: 110px;
    position: relative;
}

.teaching-tools {
    position: absolute;
    left: 0;
    height: 100%;
    width: 68%;
    text-align: left;
    overflow: hidden;
}

.video-live {
    display: block;
    position: absolute;
    left: 70%;
    height: 40%;
    width: 30%;
}

.chatroom {
    position: absolute;
    left: 70%;
    top: 40%;
    height: 60%;
    width: 30%;
    padding-top: 12px;
}

#video {
    width: 100%;
    height: 100%;
}
</style>
