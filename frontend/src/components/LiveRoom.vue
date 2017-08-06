<template>
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
                <label class="information">房间ID:{{this.id}}</label>
                <label class="information">房间名：{{this.roomName}}</label>
                <label class="information">在线人数：{{this.studentNum}}</label>
            </div>
            <div class="navigation-right">
                <Button type="primary" shape="circle" size="small">开始直播</Button>
            </div>
        </div>
        <div class="layout-header">
            <div class="teaching-area">
                <div class="choose-current">
                    <Dropdown trigger="hover" placement="right-start" @on-click="changeCurrent">
                        <Button type="ghost">
                            教学区
                            <Icon type="arrow-right-b"></Icon>
                        </Button>
                        <Dropdown-menu slot="list">
                            <Dropdown-item name="showWhiteBoard">白板</Dropdown-item>
                            <Dropdown-item name="showCodeEditor">代码编辑器</Dropdown-item>
                            <Dropdown-item name="showCourseware">课件展示</Dropdown-item>
                        </Dropdown-menu>
                    </Dropdown>
                </div>
                <template v-if="this.selected === 'showWhiteBoard'">
                    <white-board></white-board>
                </template>
                <template v-else-if="this.selected === 'showCodeEditor'">
                    <code-editor></code-editor>
                </template>
                <template v-else-if="this.selected === 'showCourseware'">
                    <file-display></file-display>
                </template>
            </div>
            <div class="composite-area">
                <div class="video-area">
                    <video-display></video-display>
                </div>
                <div class="chat-area">
                    <chat-board></chat-board>
                </div>
            </div>
        </div>
        <div>
            <page-footer></page-footer>
        </div>
    </div>
</template>

<script>
import HomePageHeader from './HomePageHeader'
import PageFooter from './PageFooter'
import FileDisplay from './FileDisplay'
import ChatBoard from './ChatBoard'
import CodeEditor from './CodeEditor'
import VideoDisplay from './VideoDisplay'
import WhiteBoard from './WhiteBoard'

export default {
    name: 'live-room',
    components: {
        HomePageHeader,
        PageFooter,
        ChatBoard,
        FileDisplay,
        CodeEditor,
        VideoDisplay,
        WhiteBoard
    },
    data: function () {
        return {
            selected: 'showWhiteBoard',
            id: '',
            roomName: '',
            teacherName: '',
            studentNum: ''
        }
    },
    created: function () {
    },
    methods: {
        changeCurrent: function (name) {
            this.selected = name
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.live-room {
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 5px;
    overflow: hidden;
}

.header {
    height: 60px;
    width: 100%;
    font-size: 40px;
}

.navigation {
    background: #efefef;
    padding: 8px 10px;
    overflow: hidden;
    display: flex;
    font-size: 15px;
}

.navigation-center {
    margin: 0 auto;
    font-size: 15px;
}

.navigation-right {
    margin-right: 15px;
    font-size: 15px;
}

.information {
    margin: 0 auto;
}

.layout-header {
    width: 1100px;
    display: flex;
    margin-left: auto;
    margin-right: auto;
}

.teaching-area {
    height: 490px;
    width: 680px;
    border: solid;
    text-align: left;
}

.composite-area {
    width: 400px;
    height: 490px;
    margin-left: 20px;
}

.video-area {
    height: 190px;
    width: 400px;
    border: solid;
}

.chat-area {
    height: 300px;
    width: 400px;
    border: solid;
}
</style>