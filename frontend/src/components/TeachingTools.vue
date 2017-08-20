<template>
    <Card class="teaching-tools">
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
                <component :is="currentTools" :roomId="this.roomId" :teacherName="this.teacherName" :username="this.username" :white-board-width="this.whiteBoardWidth" :white-board-height="this.whiteBoardHeight" :is-on-left="this.toolsOnLeft"></component>
            </keep-alive>
        </div>
    </Card>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
import * as io from 'socket.io-client'
import FileDisplay from './FileDisplay'
import WhiteBoard from './WhiteBoard'
import CodeEditor from './CodeEditor'

export default {
    name: 'teaching-tools',
    props: ['roomId', 'teacherName', 'username', 'containerHeight', 'containerWidth', 'toolsOnLeft'],
    components: {
        FileDisplay,
        CodeEditor,
        WhiteBoard
    },
    data: function () {
        return {
            currentTools: 'WhiteBoard',
            socket: '',
            whiteBoardHeight: 0,
            whiteBoardWidth: 0
        }
    },
    methods: {
        changeCurrent: function (name) {
            this.socket.emit('message', {
                'type': 'changeComponents',
                'name': name
            }, this.roomId)
        }
    },
    created: function () {
        this.socket = io.connect('http://localhost:9000')
        this.socket.emit('joinRoom', this.roomId)
    },
    mounted: function () {
        let self = this
        self.socket.on('message', function (data) {
            self.currentTools = data['name']
        })
    },
    watch: {
        containerHeight: function (newVal, oldVal) {
            this.whiteBoardWidth = newVal - 74 - 32
        },
        containerWidth: function (newVal, oldVal) {
            this.whiteBoardWidth = newVal - 32 - 32
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
