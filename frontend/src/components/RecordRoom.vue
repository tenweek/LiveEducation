<template>
    <div class="record-room">
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
                    <component :is="currentTools" :userAccount="this.userAccount" :roomId="this.roomId" :teachingToolsWidth="400" :teachingToolsHeight="400"></component>
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
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
/**
 * 录播间页面
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
            roomId: '',
            videoPath: '',
            userAccount: ''
        }
    },
    created: function () {
        let arrCookies = document.cookie.split(';')
        for (let i = 0; i < arrCookies.length; i++) {
            let arrStr = arrCookies[i].split('=')
            if (arrStr[0].replace(/(^\s*)|(\s*$)/g, '') === 'userAccount') {
                this.canWork = true
                this.userAccount = arrStr[1]
            }
        }
        this.roomId = this.$route.params.id
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
    }
}
</script>

<style scoped>
.record-room {
    border: 1px solid #d7dde4;
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


.layout-header {
    width: 78%;
    height: 78%;
    display: flex;
    margin-left: auto;
    margin-right: auto;
    margin-top: 110px;
}

.teaching-tools {
    height: 100%;
    width: 68%;
    border: solid;
    text-align: left;
    overflow: hidden;
}

.composite-container {
    width: 30%;
    height: 100%;
    margin-left: 2%;
}

.video-live {
    height: 30%;
    width: 100%;
    border: solid;
}

.chatroom {
    margin-top: 4%;
    height: 68%;
    width: 100%;
    border: solid;
}

#video {
    width: 100%;
    height: 100%;
}
</style>
