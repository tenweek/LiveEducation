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
                <label class="information">房间ID:{{ this.roomId }}</label>
                <label class="information">房间名：{{ this.roomName }}</label>
                <label class="information">在线人数：{{ this.studentNum }}</label>
            </div>
            <div class="navigation-right">
                <template v-if="this.teacherName === this.username">
                    <Button type="primary" shape="circle" size="small">开始直播</Button>
                </template>
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
                    <component :is="currentTools" :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username"></component>
                </keep-alive>
            </div>
            <div class="composite-container">
                <div class="video-live">
                    <video-display :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username"></video-display>
                </div>
                <div class="chatroom">
                    <chat-board v-on:stuNum="getNum" :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username"></chat-board>
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
            roomId: -1,
            roomName: '',
            teacherName: '',
            studentNum: '',
            username: ''
        }
    },
    created: function () {
        this.roomId = this.$route.params.id
        this.getRoomInfo()
        this.getUsername()
        window.setInterval(this.changeNum, 5000)
    },
    methods: {
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
        changeCurrent: function (name) {
            this.currentTools = name
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.live-room {
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