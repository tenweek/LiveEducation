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
                <label class="information">老师姓名：{{ this.teacherName }}</label>
                <label class="information">房间ID:{{ this.id }}</label>
                <label class="information">房间名：{{ this.roomName }}</label>
                <label class="information">在线人数：{{ this.studentNum }}</label>
            </div>
            <div class="navigation-right">
                <Button type="primary" shape="circle" size="small">开始直播</Button>
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
                <component :is="currentTools" keep-alive></component>
            </div>
            <div class="composite-container">
                <div class="video-live">
                    <video-display :id="this.id" :teacherName="this.teacherName" :username="this.username"></video-display>
                </div>
                <div class="chatroom">
                    <chat-board :id="this.id" :teacherName="this.teacherName" :username="this.username"></chat-board>
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
            currentTools: 'WhiteBoard',
            id: -1,
            roomName: '',
            teacherName: '',
            studentNum: '',
            username: ''
        }
    },
    created: function () {
        this.id = this.$route.params.id
        fetch('/getRoomInfo/', {
            method: 'post',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json, text/plain, */*',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                'roomID': this.id
            })
        }).then((response) => response.json()).then((obj) => {
            this.roomName = obj.roomName
            this.studentNum = obj.stuNum
            this.teacherName = obj.teacherName
        })
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
    methods: {
        changeCurrent: function (name) {
            this.currentTools = name
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

.teaching-tools {
    height: 490px;
    width: 680px;
    border: solid;
    text-align: left;
    overflow: hidden;
}

.composite-container {
    width: 400px;
    height: 490px;
    margin-left: 20px;
}

.video-live {
    height: 190px;
    width: 400px;
    border: solid;
}

.chatroom {
    height: 300px;
    width: 400px;
    border: solid;
}
</style>