<template>
    <Card class="teaching-tools" dis-hover>
        <div>
            <div class="choose-current">
                <Dropdown trigger="hover" placement="right-start" @on-click="changeCurrent">
                    <Button type="ghost">
                        教学区
                        <Icon type="arrow-right-b"></Icon>
                    </Button>
                    <Dropdown-menu slot="list">
                        <Dropdown-item name="WhiteBoard">白板</Dropdown-item>
                        <Dropdown-item name="CodeEditor">代码编辑器</Dropdown-item>
                        <Dropdown-item name="FileDisplay">课件展示</Dropdown-item>
                    </Dropdown-menu>
                </Dropdown>
            </div>
            <keep-alive>
                <component :is="currentTools" :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username" :white-board-width="this.whiteBoardWidth" :container-height="this.whiteBoardHeight" :is-on-left="this.toolsOnLeft"></component>
            </keep-alive>
        </div>
    </Card>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
/**
 * 教学区组件，包含白板、ppt、代码编辑器，
 * 作为子组件插入到直播间页面。
 *
 * @module TeachingTools
 * @class TeachingTools
 */
import * as io from 'socket.io-client'
import FileDisplay from './FileDisplay'
import WhiteBoard from './WhiteBoard'
import CodeEditor from './CodeEditor'

export default {
    name: 'teaching-tools',
    /**
     *表示房间ID号
     *
     * @property roomId
     * @type String
     */

    /**
     *表示创建该房间的老师名字
     *
     * @property teacherName
     * @type String
     */

    /**
     *表示进入该房间的用户名字
     *
     * @property username
     * @type String
     */

    /**
     *表示白板区域的宽，根据父组件大小动态变化
     *
     * @property teachingToolsWidth
     * @type Number
     */

    /**
     *表示白板区域的长，根据父组件大小动态变化
     *
     * @property teachingToolsHeight
     * @type Number
     */
    props: ['roomId', 'teacherName', 'username', 'containerHeight', 'containerWidth', 'toolsOnLeft'],
    components: {
        FileDisplay,
        CodeEditor,
        WhiteBoard
    },
    data: function () {
        return {
            /**
             * 表示当前选择的工具（白板、PPT、代码编辑器）
             *
             * @attribute currentTools
             * @type String
             * @default 'WhiteBoard'
             */
            currentTools: 'WhiteBoard',
            /**
             * 表示客户端，监听服务器传来的消息
             *
             * @attribute socket
             * @type Object
             * @default ''
             */
            socket: '',
            whiteBoardHeight: 0,
            whiteBoardWidth: 0
        }
    },
    /**
     * created函数，连接到socket服务器，并发送'joinRoom'消息
     *
     * @method created
     */
    created: function () {
        this.socket = io.connect('http://localhost:9000')
        this.socket.emit('joinRoom', this.roomId)
    },
    /**
     * mounted函数，当接收到'message'消息时改变相应属性值
     *
     * @method mounted
     */
    mounted: function () {
        let self = this
        self.socket.on('message', function (data) {
            self.currentTools = data['name']
        })
    },
    methods: {
        /**
         * 向服务器发送'message'消息以改变当前选中的工具
         *
         * @method changeCurrent
         */
        changeCurrent: function (name) {
            this.socket.emit('message', {
                'type': 'changeComponents',
                'name': name
            }, this.roomId)
        }
    },
    watch: {
        containerHeight: function (newVal, oldVal) {
            if (this.toolsOnLeft) {
                this.whiteBoardHeight = newVal - 96
            } else {
                this.whiteBoardHeight = newVal - 32
            }
        },
        containerWidth: function (newVal, oldVal) {
            this.whiteBoardWidth = newVal - 106
        },
        toolsOnLeft: function (newVal, oldVal) {
            if (newVal) {
                document.getElementsByClassName('choose-current')[0].style.display = 'inline-block'
            } else {
                document.getElementsByClassName('choose-current')[0].style.display = 'none'
            }
        }
    }
}
</script>

<style scoped>
.teaching-tools {
    width: 100%;
    height: 100%;
}
</style>