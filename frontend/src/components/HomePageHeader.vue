<template>
    <div class="title">
        <div class="logo">
            <a href="#">
                <div class="logo-picture">
                    <img src="../assets/rabbit.png" height="58">
                </div>
                <div class="logo-text">
                    <label>MDZZ</label>
                </div>
            </a>
        </div>
        <Row class="row">
            <Col class="navigation-center" span="19">
            <a :class="this.myOption === 1 ? 'selected' : 'navigation-bar'" href="#">
                <Icon type="home"></Icon> 首页</a> |
            <a :class="this.myOption === 2 ? 'selected' : 'navigation-bar'" href="#/live_page">
                <Icon type="university"></Icon> 直播</a> |
            <a :class="this.myOption === 3 ? 'selected' : 'navigation-bar'" href="#/record_page">
                <Icon type="videocamera"></Icon> 录播</a>
            <template v-if="this.isTeacher === true">
                |
                <a class="navigation-bar" @click="showCreateRoom = true">
                    <Icon type="ios-plus"></Icon> 创建房间
                </a>
            </template>
            <Modal v-model="showCreateRoom" title="创建房间" @on-ok="createRoom">
                <label>房间名称：</label>
                <Input v-model="roomName" size="large" placeholder="请输入房间名称"></Input>
                <br>
                <br>
                <p>上传封面图</p>
                <Upload ref="upload" :on-success="handleSuccess" :format="['jpg', 'jpeg', 'png']" :max-size="10240" :on-format-error="imgFormatError" :on-exceeded-size="handleMaxSize" name="myfile" action="/upload/">
                    <div class="upload-img">
                        <img :src="this.route">
                        <div class="upload-cover">
                            <Icon type="plus"></Icon>
                        </div>
                    </div>
                </Upload>
                <br>
                <p>上传课件</p>
                <Upload name="file" :before-upload="handleUpload" :show-upload-list="false" :on-success="upload" :format="['ppt','pptx','key','pdf']" :on-format-error="fileFormatError" action="/uploadFile/">
                    <div class="upload-file">
                        <Button type="ghost">点击选择文件&nbsp;&nbsp;
                            <Icon type="folder"></Icon>
                        </Button>
                    </div>
                </Upload>
                <div v-if="file !== null">
                    待上传文件：{{ file.name }}
                    <Button type="text" :loading="loadingStatus">
                        {{ '上传中' }}
                    </Button>
                </div>
            </Modal>
            </Col>
            <Col class="navigation-right" span="5">
            <template v-if="this.username === ''">
                <a class="navigation-right-bar" @click="login">登录</a>
                <a class="navigation-right-bar" @click="signUp">注册</a>
            </template>
            <template v-else>
                <Dropdown @on-click="dropDownClick">
                    <a class="navigation-right-bar" href="javascript:void(0)">
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
                            <Input v-model="newUsername" size="large" placeholder="请输入新的昵称"></Input>
                            <br>
                            <br>
                        </Modal>
                        <Dropdown-item name='modifyPassword'>修改密码</Dropdown-item>
                        <Dropdown-item name='logOut' divided>注销账户</Dropdown-item>
                    </Dropdown-menu>
                </Dropdown>
            </template>
            </Col>
        </Row>
    </div>
</template>

<script>
/**
 * 页面的导航栏部分，
 * 在首页、直播间、录播间、直播详情页、录播详情页作为子组件插入。
 * 包含了直播网站的logo、名字等信息，有首页、直播、录播、登录注册等选项，
 * 点击可进入相关页面。
 * 用户在登录后可以看到自己的个人信息并且有修改昵称、密码等功能，
 * 若用户拥有老师权限则可以进行创建房间。
 *
 * @module HomePageHeader
 * @class HomePageHeader
 */
import myMsg from './../warning.js'
export default {
    name: 'home-page-header',
    /**
     * 表示导航栏的选择（首页、直播、录播）
     *
     * @property myOption
     * @type Number
     */
    props: ['myOption'],
    components: {
    },
    data: function () {
        return {
            /**
             * 表示是否显示创建房间的消息框
             *
             * @attribute showCreateRoom
             * @type Boolean
             * @default false
             */
            showCreateRoom: false,
            /**
             * 表示是否显示修改昵称的消息框
             *
             * @attribute showChangeName
             * @type Boolean
             * @default false
             */
            showChangeName: false,
            /**
             * 表示当前用户是否为创建房间的老师
             *
             * @attribute isTeacher
             * @type Boolean
             * @default false
             */
            isTeacher: false,
            /**
             * 表示用户昵称
             *
             * @attribute username
             * @type String
             * @default ''
             */
            username: '',
            /**
             * 表示用户账号
             *
             * @attribute account
             * @type String
             * @default ''
             */
            account: '',
            /**
             * 表示房间名称
             *
             * @attribute roomName
             * @type String
             * @default ''
             */
            roomName: '',
            /**
             * 表示修改昵称时新输入的用户昵称
             *
             * @attribute newUsername
             * @type String
             * @default ''
             */
            newUsername: '',
            /**
             * 表示创建房间时缩略图的保存路径
             *
             * @attribute route
             * @type String
             * @default ''
             */
            route: '',
            /**
             * 表示创建房间时上传的文件
             *
             * @attribute file
             * @type null
             */
            file: null,
            hadImg: false,
            /**
             * 表示创建房间时上传文件的状态
             *
             * @attribute loadingStatus
             * @type Boolean
             * @default false
             */
            loadingStatus: false
        }
    },
    /**
     * created函数，判断用户是否登录，
     * 并且判断用户是否有老师权限。
     *
     * @method created
     */
    created: function () {
        let arrCookies = document.cookie.split(';')
        for (let i = 0; i < arrCookies.length; i++) {
            let arrStr = arrCookies[i].split('=')
            if (arrStr[0].replace(/(^\s*)|(\s*$)/g, '') === 'userAccount') {
                this.account = arrStr[1].replace(/(^\s*)|(\s*$)/g, '')
            }
        }
        if (this.account !== '') {
            fetch('/getName/', {
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
        handleMaxSize: function (file) {
            this.$Message.error('文件 ' + file.name + ' 图片太大，请上传10M以下的图片')
        },
        /**
         * 老师在创建房间上传文件时，
         * 若文件格式不正确（支持ppt、pptx、key格式），
         * 显示error消息框进行提示
         *
         * @method fileFormatError
         * @param file 表示用户想要上传的文件
         */
        fileFormatError: function (file) {
            this.file = null
            this.loadingStatus = false
            this.$Message.error('文件 ' + file.name + ' 格式不正确，请上传ppt、pptx或key格式的图片')
        },
        /**
         * 用户在创建房间上传封面图的时候，
         * 若图片格式不正确（支持jpg、png格式），
         * 显示error消息框进行提示
         *
         * @method imgFormatError
         * @param file 用户想要上传的文件
         */
        imgFormatError: function (file) {
            this.$Message.error('文件 ' + file.name + ' 格式不正确，请上传jpg或png格式的图片')
        },
        /**
         * 用户在上传文件前要进行的操作
         *
         * @method handleUpload
         * @param file 用户想要上传的文件
         */
        handleUpload: function (file) {
            this.file = file
            this.loadingStatus = true
            return true
        },
        /**
         * 用户上传文件成功时调用，弹出'上传成功'的消息框
         *
         * @method upload
         */
        upload: function () {
            this.file = null
            this.loadingStatus = false
            this.$Message.success('上传成功')
        },
        /**
         * 用户上传封面图成功时调用，获取图片地址
         *
         * @method handleSuccess
         * @param res
         * @param file 上传的图片
         */
        handleSuccess: function (res, file) {
            setTimeout(() => {
                this.$refs.upload.fileList.splice(0, 1)
                fetch('/getImg/', {
                    method: 'post',
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json, text/plain, */*',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        'account': this.account
                    })
                }).then((response) => response.json()).then((obj) => {
                    setTimeout(() => {
                        this.route = obj.route
                        this.hadImg = true
                    }, 1000)
                })
            }, 1500)
        },
        /**
         * 创建房间
         *
         * @method createRoom
         */
        createRoom: function () {
            if (this.roomName === '') {
                this.$Message.error(myMsg.room['nameNeeded'])
                return
            } else if (!this.hadImg) {
                this.$Message.error(myMsg.room['picNeeded'])
                return
            } else {
                fetch('/createRoom/', {
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
                    // 创建房间后进行房间缺少信息
                    // window.open('./#/live_room/' + obj.roomId)
                    this.hadImg = false
                    this.$Message.success(myMsg.room['create'])
                })
            }
        },
        /**
         * 修改昵称，在修改昵称的消息框中点击'OK'按钮时调用
         *
         * @method changeName
         */
        changeName: function () {
            fetch('/changeName/', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'account': this.account,
                    'newname': this.newUsername
                })
            }).then((response) => response.json()).then((obj) => {
                if (obj.result) {
                    this.username = this.newUsername
                    this.$Message.success(myMsg.account['nameChanged'])
                    this.newUsername = ''
                } else {
                    this.$Message.error(myMsg.account['nameExist'])
                    this.newUsername = ''
                }
            })
        },
        /**
         * 跳转到登录页面，点击'登录'时触发
         *
         * @method login
         */
        login: function () {
            this.$router.push({ path: '/login' })
        },
        /**
         * 跳转到注册页面，点击'注册'时触发
         *
         * @method signUp
         */
        signUp: function () {
            this.$router.push({ path: '/signup' })
        },
        /**
         * 清除cookie，点击'注销账户'时触发
         *
         * @method clearCookie
         */
        clearCookie: function () {
            let date = new Date()
            date.setTime(date.getTime() - 10000)
            document.cookie = 'userAccount=a; expires=' + date.toGMTString()
        },
        /**
         * 个人信息下拉栏的on-click响应事件
         *
         * @method dropDownClick
         * @param name 表示当前登录用户的昵称
         */
        dropDownClick: function (name) {
            if (name === 'changeName') {
                this.showChangeName = true
            } else if (name === 'modifyPassword') {
                this.clearCookie()
                this.$router.push({ path: '/reset' })
            } else {
                this.clearCookie()
                location.reload()
                this.$router.push({ path: '/' })
            }
        }
    }
}
</script>

<style scoped>
.upload-img {
    display: inline-block;
    width: 100px;
    height: 100px;
    text-align: center;
    line-height: 100px;
    border: 1px solid transparent;
    border-radius: 4px;
    overflow: hidden;
    background: #fff;
    position: relative;
    box-shadow: 0 1px 1px rgba(0, 0, 0, .2);
    margin-right: 4px;
}

.upload-img img {
    width: 100%;
    height: auto;
    margin: 0;
    line-height: 100px;
}

.upload-cover {
    display: none;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(0, 0, 0, .6);
}

.upload-img:hover .upload-cover {
    display: block;
}

.upload-cover i {
    color: #fff;
    font-size: 40px;
    cursor: pointer;
    margin: 0;
    line-height: 100px;
}

.title {
    height: 60px;
    line-height: 60px;
    width: 100%;
    padding-left: 50px;
    background: white;
    position: fixed;
    background: #22313F;
    display: flex;
    z-index: 50;
}

.logo-picture {
    float: left;
}

.logo-text {
    width: 140px;
    font-size: 28px;
    vertical-align: top;
    color: #ECFFFB;
    font-family: "宋体";
}

.row {
    width: 100%;
    min-width: 630px;
}

.navigation-center {
    font-size: 20px;
    padding-top: 14px;
    color: #9ba7b5;
    display: flex;
    padding-left: 20px;
}

.navigation-right {
    float: right;
    font-size: 20px;
    display: flex;
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

.ivu-dropdown-rel {
    height: 40px;
}

.navigation-bar:hover {
    color: gold;
}

.navigation-right-bar:hover {
    color: gold;
}

.navigation-bar {
    padding: 0 10px;
}

.selected {
    padding: 0 10px;
}

.navigation-right-bar {
    position: relative;
    top: 14px;
    padding: 0 10px;
}

#new-username {
    font-size: 15px;
}

#user {
    position: relative;
    top: 14px;
}
</style>
