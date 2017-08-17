<template>
    <div class="file-display" id="file">
        <div class="ppt-header">PPT放映</div>
        <div @click="makeFoucs" @keydown="modPicture()" tabindex="0">
            <img :src="this.route" />
        </div>
        <div class="ppt-footer">
            <div class="for-footer">
                <a class="arrow" :style="this.teacherName === this.username ? 'display:block' : 'display:none'" @click="prePicture">
                    <Icon type="arrow-left-b"></Icon>
                </a>
                <div class="for-place">
                    <select @change="changePage" id="for-select" class="ppt-select ppt-num1" :style="this.teacherName === this.username ? 'display:block' : 'display:none'">
                        <option v-for="page in this.maxPage" class="every-option">&nbsp;{{ page }}</option>
                    </select>
                    <div class="ppt-page">&nbsp;&nbsp;&nbsp;{{ this.currentPage }}&nbsp;&nbsp;of&nbsp;&nbsp;{{ this.maxPage }}&nbsp;&nbsp;&nbsp;</div>
                </div>
                <a class="arrow" :style="this.teacherName === this.username ? 'display:block' : 'display:none'" @click="nextPicture">
                    <Icon type="arrow-right-b"></Icon>
                </a>
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
            baseRoute: 'static/',
            recRoute: '',
            route: '',
            maxPage: '',
            currentPage: ''
        }
    },
    created: function () {
        this.recRoute = 'ppt/shili-'
        this.currentPage = 1
        this.maxPage = 15
        if (this.teacherName === this.username) {
            this.route = this.baseRoute + this.recRoute + this.currentPage + '.png'
        }
    },
    methods: {
        nextPicture: function () {
            if (this.currentPage < this.maxPage && this.teacherName === this.username) {
                this.currentPage = this.currentPage + 1
                this.route = this.baseRoute + this.recRoute + this.currentPage + '.png'
                this.socket.emit('fileDisplayMessage', this.currentPage, this.roomId + '.2')
            }
        },
        prePicture: function () {
            if (this.currentPage > 1 && this.teacherName === this.username) {
                this.currentPage = this.currentPage - 1
                this.route = this.baseRoute + this.recRoute + this.currentPage + '.png'
                this.socket.emit('fileDisplayMessage', this.currentPage, this.roomId + '.2')
            }
        },
        modPicture: function () {
            if (this.teacherName === this.username) {
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
        },
        changePage: function () {
            let selected = document.getElementById('for-select')
            this.currentPage = selected.selectedIndex + 1
            this.route = this.baseRoute + this.recRoute + this.currentPage + '.png'
            this.socket.emit('fileDisplayMessage', this.currentPage, this.roomId + '.2')
        }
    },
    mounted: function () {
        this.socket = io.connect('http://localhost:9000')
        let self = this
        self.socket.emit('joinForFileDisplay', this.roomId + '.2')
        if (this.teacherName !== this.username) {
            self.socket.on('fileDisplayMessage', function (msg) {
                self.currentPage = msg
                self.route = self.baseRoute + self.recRoute + self.currentPage + '.png'
            })
            self.socket.on('firstPicture', function (msg) {
                self.currentPage = msg
                self.route = self.baseRoute + self.recRoute + self.currentPage + '.png'
            })
        }
    }
}
</script>

<style scoped>
.file-display {
    width: 100%;
    height: auto;
    background: #52524E;
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
    border-radius: 20px;
}

img {
    border: 3px solid #52524E;
    height: auto;
    width: 100%;
}

.ppt-footer {
    width: 100%;
    height: 80px;
    background-color: #52524E;
    text-align: center;
    display: flex;
}

.for-footer {
    width: auto;
    height: 80px;
    margin: auto;
    display: flex;
}

.arrow {
    height: 80px;
    font-size: 60px;
    color: white;
    line-height: 80px;
}

.arrow:hover {
    color: #9A9B94;
}

.for-place {
    width: auto;
    position: relative;
    display: flex;
    margin: 0;
    height: 80px;
    font-size: 30px;
    color: white;
    line-height: 80px;
    background: #52524E;
    border: none;
}

.ppt-select {
    width: 40px;
    height: 80px;
    opacity: 0;
    position: absolute;
    left: 20px;
    z-index: 50;
}

.every-option {
    background: white;
    font-size: 10px;
}

.ppt-page {
    height: 80px;
    font-size: 30px;
    color: white;
    line-height: 80px;
    background: #52524E;
    border: none;
    text-align: right;
}
</style>