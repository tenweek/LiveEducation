<template>
    <div id="code-editor">
        <Select v-model='editorOptions.mode' placeholder="language" filterable>
            <Option v-for='mode in modeList' :value='mode.modeValue' :key='mode.modeName'>
                {{ mode.modeName }}
            </Option>
        </Select>
        <codemirror id='code' v-model='code' :options='editorOptions'></codemirror>
    </div>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
import * as io from 'socket.io-client'
export default {
    name: 'code-editor',
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
            code: '',
            editorOptions: {
                readOnly: true,
                tabSize: 4,
                mode: 'text/javascript',
                theme: 'base16-dark',
                lineNumbers: true,
                line: true,
                keyMap: 'sublime',
                extraKeys: { 'Ctrl': 'autocomplete' },
                foldGutter: true,
                gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
                styleSelectedText: true,
                highlightSelectionMatches: { showToken: /\w/, annotateScrollbar: true }
            },
            /**
             * 表示客户端，监听服务器传来的消息
             *
             * @attribute socket
             * @type Object
             * @default ''
             */
            socket: '',
            /**
             * 表示语言选择的列表
             *
             * @attribute modeList
             * @type Array
             */
            modeList: [
                {
                    modeName: 'JavaScript',
                    modeValue: 'text/javascript'
                },
                {
                    modeName: 'C/C++',
                    modeValue: 'text/x-c++src'
                },
                {
                    modeName: 'C#',
                    modeValue: 'text/x-csharp'
                },
                {
                    modeName: 'Java',
                    modeValue: 'text/x-java'
                },
                {
                    modeName: 'PHP',
                    modeValue: 'text/x-php'
                }
            ]
        }
    },
    /**
     * mounted函数，连接到socket服务器，并初始化相关数据。
     *
     * @method mounted
     */
    mounted: function () {
        let self = this
        self.socket = io.connect('http://localhost:9000')
        self.socket.emit('joinTest', self.roomId, 'code')
        self.socket.on('code', function (data) {
            self.code = data['code']
        })
    }
}
</script>

<style scoped>
#code-editor {
    width: 100%;
    height: auto;
}
</style>
