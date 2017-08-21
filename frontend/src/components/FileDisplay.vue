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
                    <Upload name="file" :before-upload="handleUpload" :show-upload-list="false" :on-success="upload" :format="['ppt','pptx','key','pdf']" :on-format-error="fileFormatError" action="/uploadFile/">
                        <div class="upload-file">
                            <Button type="ghost" style="background:white">点击上传课件&nbsp;&nbsp;
                                <Icon type="folder"></Icon>
                            </Button>
                        </div>
                    </Upload>
                    <div v-if="file !== null" style="background:white">
                        正在上传文件：{{ file.name }}
                        <Button type="text" :loading="loadingStatus" style="background:white">正在切换课件</Button>
                    </div>
                </div>
            </div>
        </template>
        <template v-else-if="this.isTeacher">
            <div class="drag-file">
                <Upload name="file" :before-upload="handleUpload" :show-upload-list="false" :on-success="upload" :format="['ppt','pptx','key','pdf']" :on-format-error="fileFormatError" type="drag" action="/uploadFile/">
                    <div class="upload-file">
                        <p>
                            <Icon type="ios-cloud-upload" size="50"></Icon>上传课件</p>
                    </div>
                </Upload>
                <div v-if="file !== null">
                    正在上传文件：{{ file.name }}
                    <Button type="text" :loading="loadingStatus">正在切换课件</Button>
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
/**
 * 实现教学区ppt等文件播放功能，
 * 作为子组件插入直播间页面。
 * 老师端可以对ppt做上下翻页等操作，
 * 学生端不能对白板操作，
 * 只能同步看到老师的操作。
 *
 * @module FileDisplay
 * @class FileDisplay
 */
import * as io from 'socket.io-client'

export default {
    name: 'file-display',
    props: ['roomId', 'teacherName', 'username', 'containerHeight', 'containerWidth', 'isOnLeft'],
    data: function () {
        return {
            /**
             * 表示客户端，监听服务器传来的消息
             *
             * @attribute socket
             * @type Object
             * @default ''
             */
            socket: '',
            /**
             * 表示存放文件的根目录
             *
             * @attribute baseRoute
             * @readOnly
             * @type String
             * @default 'static/ppt/'
             */
            baseRoute: 'static/ppt/',
            /**
             * 表示老师上传文件的完整路径
             *
             * @attribute route
             * @type String
             * @default ''
             */
            route: '',
            /**
             * 表示老师上传文件的最大页数
             *
             * @attribute maxPage
             * @type String
             * @default ''
             */
            maxPage: '',
            /**
             * 表示当前页码数
             *
             * @attribute currentPage
             * @type String
             * @default ''
             */
            currentPage: '',
            /**
             * 表示当前用户是否是创建房间的老师
             *
             * @attribute isTeacher
             * @type Boolean
             * @default false
             */
            isTeacher: false,
            /**
             * 表示上传的文件
             *
             * @attribute file
             * @type null
             */
            file: null,
            /**
             * 表示上传文件的状态
             *
             * @attribute loadingStatus
             * @type Boolean
             * @default false
             */
            loadingStatus: false,
            /**
             * 表示上传文件的数量
             *
             * @attribute fileNum
             * @type Number
             * @default 0
             */
            fileNum: 0,
            /**
             * 表示老师的ID号
             *
             * @attribute teacherId
             * @type String
             * @default ''
             */
            teacherId: ''
        }
    },
    /**
     * created函数，如果用户是创建房间的老师，
     * 获取上传的文件信息，并设置当且页为第一页。
     *
     * @method created
     */
    created: function () {
        if (this.teacherName === this.username) {
            this.currentPage = 1
            this.isTeacher = true
            this.getTeahcerFileInfo()
        }
    },
    /**
     * mounted函数，初始化相关数据，客户端监听服务器消息
     *
     * @method mounted
     */
    mounted: function () {
        this.socket = io.connect('http://localhost:9000')
        let self = this
        if (this.teacherName === this.username) {
            self.isTeacher = true
        }
        self.socket.emit('joinForFileDisplay', self.roomId + '.2', self.isTeacher)
        if (!self.isTeacher) {
            self.socket.on('message', function (data) {
                self.teacherId = data['teacherId']
                self.fileNum = data['fileNum']
                self.currentPage = data['currentPage']
                self.maxPage = data['maxPage']
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
    },
    methods: {
        /**
         * 获取上传文件的信息，
         * 在created函数中调用
         *
         * @method getTeahcerFileInfo
         */
        getTeahcerFileInfo: function () {
            fetch('/getTeacherFileInfo/', {
                method: 'post',
                mode: 'cors',
                credentials: 'same-origin',
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
                this.route = this.baseRoute + this.teacherId + 'and' + this.fileNum + '/user-' + this.currentPage + '.png'
                this.socket.emit('message', {
                    'type': 'file',
                    'teacherId': this.teacherId,
                    'fileNum': this.fileNum,
                    'currentPage': this.currentPage,
                    'maxPage': this.maxPage
                }, this.roomId + '.2')
            })
        },
        /**
         * 上传文件时，若文件格式不正确，给出提示
         *
         * @method fileFormatError
         * @param file 表示用户当前想要上传的文件
         */
        fileFormatError: function (file) {
            this.file = null
            this.loadingStatus = false
            this.$Message.error('文件格式不正确' + '文件 ' + file.name + ' 格式不正确，请上传 ppt  pptx  pdf 或 key 格式的图片。')
        },
        /**
         * 在上传文件之前要进行的操作
         *
         * @method handleUpload
         * @param file 表示用户将要上传的文件
         * @return true
         */
        handleUpload: function (file) {
            this.file = file
            this.loadingStatus = true
            return true
        },
        /**
         * 上传文件成功时调用，获取文件信息
         * 并显示上传成功的消息框。
         *
         * @method upload
         */
        upload: function () {
            this.file = null
            this.loadingStatus = false
            this.getTeahcerFileInfo()
            this.$Message.success('上传成功')
        },
        /**
         * 老师点击下一页按钮或是按下键盘"向下"或"向左"键时响应，
         * 如果当前页不是最后一页，则进行翻页进入下一页的操作
         *
         * @method nextPicture
         */
        nextPicture: function () {
            if (this.currentPage < this.maxPage && this.isTeacher) {
                this.currentPage = this.currentPage + 1
                this.route = this.baseRoute + this.teacherId + 'and' + this.fileNum + '/user-' + this.currentPage + '.png'
                this.socket.emit('message', {
                    'type': 'file',
                    'teacherId': this.teacherId,
                    'fileNum': this.fileNum,
                    'currentPage': this.currentPage,
                    'maxPage': this.maxPage
                }, this.roomId + '.2')
            }
        },
        /**
         * 老师点击上一页按钮或是按下键盘"向上"或"向左"键时响应，
         * 如果当前页不是第一页，则进行返回到上一页的操作
         *
         * @method prePicture
         */
        prePicture: function () {
            if (this.currentPage > 1 && this.isTeacher) {
                this.currentPage = this.currentPage - 1
                this.route = this.baseRoute + this.teacherId + 'and' + this.fileNum + '/user-' + this.currentPage + '.png'
                this.socket.emit('message', {
                    'type': 'file',
                    'teacherId': this.teacherId,
                    'fileNum': this.fileNum,
                    'currentPage': this.currentPage,
                    'maxPage': this.maxPage
                }, this.roomId + '.2')
            }
        },
        /**
         * 当点击 时触发，
         *
         * @method modPicture
         */
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
        /**
         * 当点击 时触发，
         *
         * @method makeFocus
         */
        makeFoucs: function () {
            let getfocus = document.getElementById('file')
            getfocus.focus()
        },
        /**
         * 改变当前页到指定页码
         *
         * @method changePage
         */
        changePage: function () {
            let selected = document.getElementById('for-select')
            this.currentPage = selected.selectedIndex + 1
            this.route = this.baseRoute + this.teacherId + 'and' + this.fileNum + '/user-' + this.currentPage + '.png'
            this.socket.emit('message', {
                'type': 'file',
                'teacherId': this.teacherId,
                'fileNum': this.fileNum,
                'currentPage': this.currentPage,
                'maxPage': this.maxPage
            }, this.roomId + '.2')
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

.upload-file Icon {
    color: #3399ff;
    font-size: 100px;
    line-height: 400px;
}

.upload-file p {
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
