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
            socket: '',
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
    mounted: function () {
        let self = this
        self.socket = io.connect('http://localhost:9000')
        self.socket.emit('joinTest', self.roomId, self.userAccount)
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
