<template>
    <div class="title">
        <div class="logo">
            <a href="#">
                <img src="../assets/rabbit.png" height="60">
                <label id="mdzz">MDZZ</label>
            </a>
        </div>
        <div class="navigation-center">
            <a :class="this.myOption === 1 ? 'selected' : 'navigation-bar'" href="#">
                <Icon type="home"></Icon> 首页</a> |
            <a :class="this.myOption === 2 ? 'selected' : 'navigation-bar'" href="#/live_page">
                <Icon type="university"></Icon> 直播</a> |
            <a :class="this.myOption === 3 ? 'selected' : 'navigation-bar'" href="#/record_page">
                <Icon type="videocamera"></Icon> 录播</a> |
            <template v-if="this.isTeacher === true">
                <a class="navigation-bar" @click="showCreateRoom = true">
                    <Icon type="ios-plus"></Icon> 创建房间</a>
            </template>
            <Modal v-model="showCreateRoom" title="创建房间" @on-ok="createRoom">
                <label>房间名称：</label>
                <Input v-model="roomName" size="large" placeholder="请输入房间名称"></Input>
                <br>
                <br>
                <p>上传课件</p>
                <Upload action="//jsonplaceholder.typicode.com/posts/">
                    <div class="upload">
                        <Button type="ghost">点击选择文件&nbsp;&nbsp;
                            <Icon type="folder"></Icon>
                        </Button>
                    </div>
                </Upload>
                <br>
                <p>上传封面图</p>
                <Upload action="//jsonplaceholder.typicode.com/posts/">
                    <div class="upload">
                        <Button type="ghost">
                            点击选择图片&nbsp;&nbsp;
                            <Icon type="image"></Icon>
                        </Button>
                    </div>
                </Upload>
            </Modal>
        </div>
        <div class="navigation-right">
            <template v-if="this.username === ''">
                <a class="navigation-bar" @click="login">登录</a> |
                <a class="navigation-bar" @click="signUp">注册</a>
            </template>
            <template v-else>
                <Dropdown @on-click="dropDownClick">
                    <a class="navigation-bar" href="javascript:void(0)">
                        {{ username }}
                        <Icon type="arrow-down-b"></Icon>
                    </a>
                    <Dropdown-menu slot="list">
                        <Dropdown-item name='changeName'>修改昵称</Dropdown-item>
                        <Modal v-model="showChangeName" title="修改昵称" @on-ok="changeName">
                            <br>
                            <label id="new-username">请输入新的昵称：</label>
                            <br>
                            <br>
                            <Input v-model="newUserName" size="large" placeholder="请输入新的昵称"></Input>
                            <br>
                            <br>
                        </Modal>
                        <Dropdown-item name='modifyPassword'>修改密码</Dropdown-item>
                        <Dropdown-item name='logOut'>注销账户</Dropdown-item>
                    </Dropdown-menu>
                </Dropdown>
            </template>
        </div>
    </div>
</template>

<script>
export default {
    name: 'home-page-header',
    props: ['myOption'],
    components: {
    },
    data: function () {
        return {
            showCreateRoom: false,
            showChangeName: false,
            isTeacher: false,
            username: '',
            account: '',
            roomName: '',
            newUserName: ''
        }
    },
    created: function () {
        let arrCookies = document.cookie.split(';')
        for (let i = 0; i < arrCookies.length; i++) {
            let arrStr = arrCookies[i].split('=')
            if (arrStr[0].replace(/(^\s*)|(\s*$)/g, '') === 'userAccount') {
                this.account = arrStr[1].replace(/(^\s*)|(\s*$)/g, '')
            }
        }
        if (this.account !== '') {
            fetch('getName', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ 'account': this.account })
            }).then((response) => response.json()).then((obj) => {
                this.username = obj.name
                this.isTeacher = obj.isTeacher
            })
        }
    },
    methods: {
        createRoom: function () {
            fetch('createRoom', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'roomName': this.roomName,
                    'account': this.account
                })
            }).then((response) => response.json()).then((obj) => {
                // 创建房间后自动进入该房间 目前还没做
                this.$Message.success(obj.msg)
            })
        },
        changeName: function () {
            fetch('changeName', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'account': this.account,
                    'newname': this.newUserName
                })
            }).then((response) => response.json()).then((obj) => {
                this.username = this.newUserName
                this.$Message.success('您已成功修改昵称！')
            })
        },
        login: function () {
            this.$router.push({ path: '/login' })
        },
        signUp: function () {
            this.$router.push({ path: '/signup' })
        },
        dropDownClick: function (name) {
            if (name === 'changeName') {
                this.showChangeName = true
            } else if (name === 'modifyPassword') {
                let date = new Date()
                date.setTime(date.getTime() - 10000)
                document.cookie = 'userAccount=a; expires=' + date.toGMTString()
                this.$router.push({ path: '/reset' })
            } else {
                let date = new Date()
                date.setTime(date.getTime() - 10000)
                document.cookie = 'userAccount=a; expires=' + date.toGMTString()
                location.reload()
                this.$router.push({ path: '/' })
            }
        }
    }
}
</script>

<style scoped>
.title {
    height: 60px;
    line-height: 60px;
    width: 100%;
    padding-left: 30px;
    background: white;
    position: fixed;
    background: #22313F;
    overflow: hidden;
    display: flex;
    z-index: 50;
}

.logo {
    width: 180px;
    height: 100%;
}

#mdzz {
    color: #ECFFFB;
    vertical-align: top;
    font-family: "Comic Sans MS";
    font-size: 35px;
}

.navigation-center {
    font-size: 20px;
    padding-top: 14px;
    color: #9ba7b5;
    margin-left: 20px;
}

.navigation-right {
    float: right;
    margin-right: 15px;
    font-size: 20px;
    padding-top: 14px;
    position: relative;
    margin-left: 45%;
}

.username {
    color: #E4F1FE;
}

.navigation-center a {
    color: #E4F1FE;
}

.navigation-center .selected {
    color: gold;
}

.navigation-right a {
    color: #E4F1FE;
}

.navigation-bar:hover {
    color: gold;
}

#new-username {
    font-size: 15px;
}
</style>