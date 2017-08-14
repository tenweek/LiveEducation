<template>
    <div class="file-display" id="file" @click="makeFoucs" @keydown="modPicture()" tabindex="0">
        <img :src="this.route" width="675px" class="my-img" />
    </div>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
import * as io from 'socket.io-client'

export default {
    name: 'file-display',
    props: ['id', 'teacherName', 'username'],
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
            if (this.nowNum < this.maxNum) {
                this.nowNum = this.nowNum + 1
                this.route = this.baseRoute + this.recRoute + this.nowNum + '.png'
                this.socket.emit('fileDisplayMessage', this.route, this.id + '.2', this.id)
            }
        },
        prePicture: function () {
            if (this.nowNum > 1) {
                this.nowNum = this.nowNum - 1
                this.route = this.baseRoute + this.recRoute + this.nowNum + '.png'
                this.socket.emit('fileDisplayMessage', this.route, this.id + '.2', this.id)
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
            var getfocus = document.getElementById('file')
            getfocus.focus()
        }
    },
    mounted: function () {
        this.socket = io.connect('http://localhost:9000')
        var self = this
        this.socket.emit('joinFileDisplay', this.id + '.2', this.id)
        this.socket.on('fileDisplayMessage', function (msg) {
            if (!self.isTeacher) {
                self.route = msg
            }
        })
        if (!this.isTeacher) {
            this.socket.on('firstPicture', function (msg) {
                self.route = msg
            })
        }
    }
}
</script>

<style scoped>
.my-img {
    border: 3px solid #000;
}

.file-display {
    width: 680px;
    height: 480px;
}
</style>