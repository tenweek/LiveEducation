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
/**
 * 实现教学区ppt等文件播放的复现，
 * 作为子组件插入录播间页面，
 * 用户不能进行任何操作。
 *
 * @module FileDisplayForRecord
 * @class FileDisplayForRecord
 */
import * as io from 'socket.io-client'

export default {
    name: 'file-display',
    /**
     * 表示房间ID信息
     *
     * @property roomId
     * @type String
     */

    /**
     * 表示用户账号信息
     *
     * @property userAccount
     * @type String
     */
    props: ['roomId', 'userAccount'],
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
             * 表示上传文件的数量
             *
             * @attribute fileNum
             * @type Number
             * @default 0
             */
            fileNum: 0
        }
    },
    /**
     * mounted函数，初始化相关数据，客户端监听服务器消息
     *
     * @method mounted
     */
    mounted: function () {
        let self = this
        self.socket = io.connect('http://localhost:9000')
        self.socket.emit('joinTest', this.roomId, 'file')
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
