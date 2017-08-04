<template>
    <div class="title">
        <div class="logo">
            <a href="#">
                <img src="../assets/rabbit.png" height="60">
                <label id="mdzz">MDZZ</label>
            </a>
        </div>
        <div class="navigation-center">
            <a class="navigation-bar" href="#">
                <Icon type="home"></Icon> 首页</a> |
            <a class="navigation-bar" href="#">
                <Icon type="university"></Icon> 直播</a> |
            <a class="navigation-bar" href="#">
                <Icon type="videocamera"></Icon> 录播</a> |
            <a class="navigation-bar" @click="modal = true">
                <Icon type="ios-plus"></Icon> 创建房间</a>
            <Modal v-model="modal" title="创建房间" @on-ok="ok" @on-cancel="cancel">
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
            <template v-if="this.name === ''">
                <a class="navigation-bar" id="login" @click="login">登录</a> |
                <a class="navigation-bar" @click="signUp">注册</a>
            </template>
    
            <template v-else>
                <Dropdown>
                    <a class="navigation-bar" href=" ">
                        {{ name }}
                        <Icon type="arrow-down-b"></Icon>
                    </a>
                    <Dropdown-menu slot="list">
                        <Dropdown-item>修改昵称</Dropdown-item>
                        <Dropdown-item>
                            <label @click="resetPasswd">修改密码</label>
                        </Dropdown-item>
                        <Dropdown-item>
                            <label @click="signOut">注销账户</label>
                        </Dropdown-item>
                    </Dropdown-menu>
                </Dropdown>
            </template>
        </div>
    </div>
</template>

<script>
export default {
    name: 'home-page-header',
    components: {
    },
    data: function () {
        return {
            modal: false,
            roomName: '',
            name: '',
            account: ''
        }
    },
    created: function () {
        this.name = document.cookie.split(';')[0].split('=')[0]
        this.account = document.cookie.split(';')[0].split('=')[1]
    },
    methods: {
        ok: function () {
            this.$Message.info('您已成功创建房间！')
        },
        cancel: function () {
            this.$Message.info('点击了取消')
        },
        login: function () {
            if (this.name) {
                this.$Message.error('已经登录过了！')
            } else {
                this.$router.push({ path: '/login' })
            }
        },
        resetPasswd: function () {
            this.$router.push({ path: '/reset' })
        },
        signUp: function () {
            this.$router.push({ path: '/signup' })
        },
        signOut: function () {
            var date = new Date()
            date.setTime(date.getTime() - 10000)
            document.cookie = this.name + '=a; expires=' + date.toGMTString()
            window.location.reload()
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
    min-width: 1300px;
    display: flex;
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

.navigation-center a {
    color: #E4F1FE;
}

.navigation-right a {
    color: #E4F1FE;
}

.navigation-bar:hover {
    color: gold;
}
</style>
