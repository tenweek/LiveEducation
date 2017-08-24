<template>
<div id="bg">
    <div id="record-room">
        <div class="header">
            <home-page-header></home-page-header>
        </div>
        <div class="navigation">
            <div class="welcome">
                <Icon type="university"></Icon>
                <label>欢迎进入录播间 !</label>
            </div>
        </div>
        <div class="layout-header">
            <div class="teaching-tools">
                <div class="choose-current">
                    <Button type="ghost">
                        教学区
                        <Icon type="arrow-right-b"></Icon>
                    </Button>
                </div>
                <keep-alive>
                    <component :is="currentTools" :userAccount="this.userAccount" :roomId="this.roomId" :teachingToolsWidth="this.teachingToolsWidth" :teachingToolsHeight="this.teachingToolsHeight"></component>
                </keep-alive>
            </div>
            <div class="composite-container">
                <div class="video-live">
                    <video :src=videoPath id="video" autoplay="autoplay"></video>
                </div>
                <div class="chatroom">
                    <chat-board-for-record :roomId="this.roomId" :userAccount="this.userAccount"></chat-board-for-record>
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
            userAccount: ''
            teachingToolsHeight: 0,
            teachingToolsWidth: 0
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
        self.socket.emit('joinTest', self.roomId, self.userAccount + 't')
        self.socket.on('changeCurrent', function (data) {
            self.currentTools = data['name'] + 'ForRecord'
        })
        window.onresize = () => {
            let self = this
            this.resize(self)
        }
    },
    methods: {
        resize: function (self) {
            document.getElementById('bg').style.height = window.innerHeight + 'px'
            document.getElementById('bg').style.width = window.innerWidth + 'px'
            let unit = Math.min(window.innerWidth / 1.33, window.innerHeight)
            document.getElementById('record-room').style.width = (1.33 * unit) + 'px'
            document.getElementById('record-room').style.height = unit + 'px'
            self.teachingToolsWidth = document.getElementById('teaching-tools').clientWidth
            self.teachingToolsHeight = document.getElementById('teaching-tools').clientHeight
        }
    }
}
</script>

<style scoped>
#bg {
    min-width: 800px;
    min-height: 600px;
}

.record-room {
    background: transparent;
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


.layout-header {
    width: 98%;
    height: 78%;
    min-width: 800px;
    display: flex;
    margin-left: auto;
    margin-right: auto;
    margin-top: 110px;
}

.teaching-tools {
    height: 100%;
    width: 65%;
    text-align: left;
    overflow: hidden;
}

.composite-container {
    width: 30%;
    height: 100%;
    margin-left: 2%;
}

.video-live {
    height: 40%;
    width: 100%;
}

.chatroom {
    height: 60%;
    width: 100%;
    padding-top: 12px;
}

#video {
    width: 100%;
    height: 100%;
}
</style>
