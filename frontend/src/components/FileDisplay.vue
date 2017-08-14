<template>
    <div class="file-display" id="file" @click="makeFoucs" @keydown="modPicture()" tabindex="0">
        <div class="ppt-header">PPT放映</div>
        <img :src="this.route" width="100%" class="my-img" />
        <div class="ppt-footer">
            <div class="for-footer">
        <a class="arrow" :style="this.isTeacher ? 'display:block' : 'display:none'" @click="prePicture"><Icon type="arrow-left-b"></Icon></a>
        <div class="ppt-num">&nbsp;&nbsp;{{this.nowNum}}&nbsp;of&nbsp;{{this.maxNum}}&nbsp;&nbsp;</div>
        <a class="arrow" :style="this.isTeacher ? 'display:block' : 'display:none'" @click="nextPicture"><Icon type="arrow-right-b"></Icon></a>
            </div>
        </div>
    </div>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
import * as io from 'socket.io-client'

export default {
    name: 'file-display',
    props: ['roomId', 'teacherName', 'username'],
    data: function () {
        return {
            socket: '',
            baseRoute: '/static/',
            recRoute: '',
            route: '',
            maxNum: '',
            nowNum: '',
            isTeacher: false
        }
    },
    created: function () {
        this.recRoute = 'ppt/shili-'
        this.nowNum = 1
        this.maxNum = 15
        if (this.teacherName === this.username) {
            this.isTeacher = true
            this.route = this.baseRoute + this.recRoute + this.nowNum + '.png'
        }
    },
    methods: {
        nextPicture: function () {
            if (this.nowNum < this.maxNum && this.isTeacher) {
                this.nowNum = this.nowNum + 1
                this.route = this.baseRoute + this.recRoute + this.nowNum + '.png'
                this.socket.emit('fileDisplayMessage', this.route, this.roomId + '.2', this.roomId)
            }
        },
        prePicture: function () {
            if (this.nowNum > 1 && this.isTeacher) {
                this.nowNum = this.nowNum - 1
                this.route = this.baseRoute + this.recRoute + this.nowNum + '.png'
                this.socket.emit('fileDisplayMessage', this.route, this.roomId + '.2', this.roomId)
            }
        },
        modPicture: function () {
            if (this.isTeacher) {
                if (event.keyCode === 39 || event.keyCode === 40) {
                    this.nextPicture()
                }
                if (event.keyCode === 37 || event.keyCode === 38) {
                    this.prePicture()
                }
            }
        },
        makeFoucs: function () {
            let getfocus = document.getElementById('file')
            getfocus.focus()
        }
    },
    mounted: function () {
        this.socket = io.connect('http://localhost:9000')
        let self = this
        self.socket.emit('joinForFileDisplay', this.roomId + '.2', this.roomId)
        self.socket.on('fileDisplayMessage', function (msg) {
            if (!self.isTeacher) {
                self.route = msg
            }
        })
        if (!self.isTeacher) {
            self.socket.on('firstPicture', function (msg) {
                self.route = msg
                console.log(msg)
            })
        }
    }
}
</script>

<style scoped>
.my-img {
    border: 3px solid #52524E;
}

.file-display {
    width: 100%;
    height: auto;
    background: #52524E;
}

.for-footer {
    width: auto;
    height: 80px;
    margin: auto;
    background: #52524E;
    display: flex;
}

.arrow {
    height: 80px;
    font-size: 60px;
    color: white;
    line-height: 80px;
}

.ppt-num {
    height: 80px;
    font-size: 30px;
    color: white;
    line-height: 80px;
}

.arrow:hover {
    color: #9A9B94;
}

.ppt-header {
    background-color: #52524E;
    width: 100%;
    height: 50px;
    border-color: #52524E;
    font-size: 20px;
    color: white;
    text-align: center;
    line-height: 50px;
    margin-top: 20px;
}

.ppt-footer {
    width: 100%;
    height: 80px;
    background-color: #52524E;
    text-align: center;
    display: flex;
}
</style>