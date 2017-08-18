<template>
    <div>
        <template v-if="this.fileNum > 0">
            <div class="file-display" id="file">
                <div class="ppt-header">PPT放映</div>
                <div @click="makeFoucs" @keydown="modPicture()" tabindex="0">
                    <img :src="this.route" />
                </div>
                <div class="ppt-footer">
                    <div class="for-footer">
                        <a class="arrow" :style="this.isTeacher ? 'display:block' : 'display:none'" @click="prePicture">
                            <Icon type="arrow-left-b"></Icon>
                        </a>
                        <div class="for-place">
                            <select @change="changePage" id="for-select" class="ppt-select ppt-num1" :style="this.isTeacher ? 'display:block' : 'display:none'">
                                <option v-for="page in this.maxPage" class="every-option">&nbsp;{{ page }}</option>
                            </select>
                            <div class="ppt-page">&nbsp;&nbsp;&nbsp;{{ this.currentPage }}&nbsp;&nbsp;of&nbsp;&nbsp;{{ this.maxPage }}&nbsp;&nbsp;&nbsp;</div>
                        </div>
                        <a class="arrow" :style="this.isTeacher ? 'display:block' : 'display:none'" @click="nextPicture">
                            <Icon type="arrow-right-b"></Icon>
                        </a>
                    </div>
                </div>
                <div :style="this.isTeacher ? 'display:block':'display:none'">
                    <Upload name="file"
                        :before-upload="handleUpload"
                        :show-upload-list="false"
                        :on-success="upload"
                        :format="['ppt','pptx','key','pdf']"
                        :on-format-error="fileFormatError"
                        action="/uploadFile/">
                        <div class="upload-file">
                            <Button type="ghost" style="background:white">点击上传课件&nbsp;&nbsp;
                                <Icon type="folder"></Icon>
                            </Button>
                        </div>
                    </Upload>
                    <div v-if="file !== null" style="background:white">
                        正在上传文件：{{ file.name }} 
                        <Button type="text" :loading="loadingStatus" style="background:white">上传中</Button>
                    </div>
                </div>
            </div>
        </template>
        <template v-else-if="this.isTeacher">
            <div class="drag-file">
                <Upload
                    name="file"
                    :before-upload="handleUpload"
                    :show-upload-list="false"
                    :on-success="upload"
                    :format="['ppt','pptx','key','pdf']"
                    :on-format-error="fileFormatError"
                    type="drag"
                    action="/uploadFile/">
                    <div class="upload-file">
                        <p><Icon type="ios-cloud-upload" size="50"></Icon>上传课件</p>
                    </div>
                </Upload>
                <div v-if="file !== null">
                    正在上传文件：{{ file.name }} 
                    <Button type="text" :loading="loadingStatus">上传中</Button>
                </div>
            </div>
        </template>
        <template v-else>
            <div>目前还没有课件，请等待老师上传！！！</div>
        </template>
    </div>
</template>

<script>
export default {

}
</scriptdiv>
</style>

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
            baseRoute: 'static/ppt/',
            route: '',
            maxPage: '',
            currentPage: '',
            isTeacher: false,
            file: null,
            loadingStatus: false,
            fileNum: 0,
            teacherId: ''
        }
    },
    created: function () {
        if (this.teacherName === this.username) {
            this.isTeacher = true
            this.getTeahcerFileInfo()
        }
    },
    methods: {
        getTeahcerFileInfo () {
            fetch('/getTeacherFileInfo/', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'name': this.teacherName
                })
            }).then((response) => response.json()).then((obj) => {
                this.teacherId = obj.teacherId
                this.fileNum = obj.fileNum
                this.maxPage = obj.maxPage
                this.currentPage = 1
                this.route = this.baseRoute + this.teacherId + 'and' +this.fileNum + '/user-' + this.currentPage + '.png'
                this.socket.emit('fileDisplayMessage', this.teacherId, this.fileNum, this.currentPage, this.maxPage, this.roomId + '.2', this.roomId)
            })
        },
        fileFormatError (file) {
            this.file = null;
            this.loadingStatus = false;
            this.$Message.error('文件格式不正确'+'文件 ' + file.name + ' 格式不正确，请上传 ppt  pptx  pdf 或 key 格式的图片。');
        },
        handleUpload (file) {
            this.file = file;
            this.loadingStatus = true;
            return true;
        },
        upload () {
                this.file = null;
                this.loadingStatus = false;
                this.getTeahcerFileInfo()
                this.$Message.success('上传成功')
        },
        nextPicture: function () {
            if (this.currentPage < this.maxPage && this.isTeacher) {
                this.currentPage = this.currentPage + 1
                this.route = this.baseRoute + this.teacherId + 'and' +this.fileNum + '/user-' + this.currentPage + '.png'
                this.socket.emit('fileDisplayMessage', this.teacherId, this.fileNum, this.currentPage, this.maxPage, this.roomId + '.2', this.roomId)
            }
        },
        prePicture: function () {
            if (this.currentPage > 1 && this.isTeacher) {
                this.currentPage = this.currentPage - 1
                this.route = this.baseRoute + this.teacherId + 'and' +this.fileNum + '/user-' + this.currentPage + '.png'
                this.socket.emit('fileDisplayMessage', this.teacherId, this.fileNum, this.currentPage, this.maxPage, this.roomId + '.2', this.roomId)
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
        },
        changePage: function () {
            let selected = document.getElementById('for-select')
            this.currentPage = selected.selectedIndex + 1
            this.route = this.baseRoute + this.teacherId + 'and' +this.fileNum + '/user-' + this.currentPage + '.png'
            this.socket.emit('fileDisplayMessage', this.teacherId, this.fileNum, this.currentPage, this.maxPage, this.roomId + '.2', this.roomId)
        }
    },
    mounted: function () {
        this.socket = io.connect('http://localhost:9000')
        let self = this
        if (this.teacherName === this.username) {
            self.isTeacher = true
        }
        self.socket.emit('joinForFileDisplay', self.roomId + '.2', self.roomId, self.isTeacher)
        if (!self.isTeacher) {
            self.socket.on('fileDisplayMessage', function (teacherId, fileNum, currentPage, maxPage) {
                self.teacherId = teacherId
                self.fileNum = fileNum
                self.currentPage = currentPage
                self.maxPage = maxPage
                self.route = self.baseRoute + self.teacherId + 'and' + self.fileNum + '/user-' + self.currentPage + '.png'
            })
            self.socket.on('firstPicture', function (teacherId, fileNum, currentPage, maxPage) {
                self.teacherId = teacherId
                self.fileNum = fileNum
                self.currentPage = currentPage
                self.maxPage = maxPage
                self.route = self.baseRoute + self.teacherId + 'and' + self.fileNum + '/user-' + self.currentPage + '.png'
            })
        }
    }
}
</script>

<style scoped>
.drag-file {
    width: 400px;
    height: 400px;
    border: 2px dashed black;
    margin: auto;
}

.upload-file Icon{
    color: #3399ff;
    font-size: 100px;
    line-height: 400px;
}

.upload-file p{
    color: #3399ff;
    font-size: 20px;
    line-height: 400px;
}

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