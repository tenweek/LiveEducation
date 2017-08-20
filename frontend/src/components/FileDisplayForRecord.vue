<template>
    <div>
        <template v-if="this.fileNum > 0">
            <div class="file-display" id="file">
                <div class="ppt-header">PPT放映</div>
                <div>
                    <img :src="this.route" />
                </div>
                <div class="ppt-footer">
                    <div class="for-footer">
                        <div class="for-place">
                            <div class="ppt-page">&nbsp;&nbsp;&nbsp;{{ this.currentPage }}&nbsp;&nbsp;of&nbsp;&nbsp;{{ this.maxPage }}&nbsp;&nbsp;&nbsp;</div>
                        </div>
                    </div>
                </div>
            </div>
        </template>
        <template v-else>
            <div>目前还没有课件，请等待老师上传！！！</div>
        </template>
    </div>
</template>


<script src="/socket.io/socket.io.js"></script>
<script>
import * as io from 'socket.io-client'

export default {
    name: 'file-display',
    props: ['roomId'],
    data: function () {
        return {
            socket: '',
            baseRoute: 'static/ppt/',
            route: '',
            maxPage: '',
            currentPage: '',
            fileNum: 0
        }
    },
    mounted: function () {
        let self = this
        self.socket = io.connect('http://localhost:9000')
        self.socket.emit('joinTest', this.roomId)
        self.socket.on('filedisplay', function (data) {
            self.teacherId = data['teacherId']
            self.fileNum = data['fileNum']
            self.currentPage = data['currentPage']
            self.maxPage = data['maxPage']
            self.route = self.baseRoute + self.teacherId + 'and' + self.fileNum + 'and' + self.roomId + '/user-' + self.currentPage + '.png'
        })
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
