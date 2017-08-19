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
                    <Dropdown trigger="hover" placement="right-start" @on-click="changeCurrent">
                        <Button type="ghost">
                            教学区
                            <Icon type="arrow-right-b"></Icon>
                        </Button>
                        <Dropdown-menu slot="list">
                            <Dropdown-item name="WhiteBoard">白板</Dropdown-item>
                            <Dropdown-item name="CodeEditor">代码编辑器</Dropdown-item>
                            <Dropdown-item name="FileDisplay">课件展示</Dropdown-item>
                        </Dropdown-menu>
                    </Dropdown>
                </div>
                <keep-alive>
                    <component :is="currentTools" :roomId="this.roomId" :teachingToolsWidth="400" :teachingToolsHeight="400"></component>
                </keep-alive>
            </div>
            <div class="composite-container">
                <div class="video-live"></div>
                <div class="chatroom">
                    <chat-board-for-record :roomId="this.roomId"></chat-board-for-record>
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
import HomePageHeader from './HomePageHeader'
import PageFooter from './PageFooter'
import ChatBoardForRecord from './ChatBoardForRecord'
import FileDisplayForRecord from './FileDisplayForRecord'
import WhiteBoardForRecord from './WhiteBoardForRecord'
import * as io from 'socket.io-client'

export default {
    name: 'record-room',
    components: {
        HomePageHeader,
        PageFooter,
        ChatBoardForRecord,
        FileDisplayForRecord,
        WhiteBoardForRecord
    },
    data: function () {
        return {
            currentTools: 'WhiteBoardForRecord'
        }
    },
    mounted: function () {
        let self = this
        self.socket = io.connect('http://localhost:9000')
        self.socket.emit('joinTest', 888)
        self.socket.on('changeCurrent', function (data) {
            self.currentTools = data['name'] + 'ForRecord'
        })
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
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
</style>
