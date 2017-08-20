<template>
    <div class="code-editor">
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
/**
 * 实现教学区代码编辑器功能，
 * 作为子组件插入直播间页面。
 * 老师端可以选择不同语言输入代码，
 * 并同步到学生端。
 * 学生端不能对代码编辑器进行操作，
 * 只能同步看到老师的操作。
 *
 * @module CodeEditor
 * @class CodeEditor
 */
import * as io from 'socket.io-client'
export default {
    name: 'code-editor',
    props: ['roomId', 'teacherName', 'username'],
    data: function () {
        return {
            code: 'const a = 10   123456789',
            editorOptions: {
                readOnly: false,
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
                    modeValue: 'application/x-httpd-php'
                }
            ]
        }
    },
    mounted: function () {
        let self = this
        self.socket = io.connect('http://localhost:9000')
        self.socket.emit('joinForCodeEditor', self.roomId + '.3')
        if (self.username !== self.teacherName) {
            self.editorOptions.readOnly = true
            self.socket.on('message', function (data) {
                self.code = data['code']
            })
        }
    },
    watch: {
        code: function (newcode, oldcode) {
            if (newcode !== oldcode && this.username === this.teacherName) {
                this.socket.emit('message', {
                    type: 'code',
                    code: newcode
                }, this.roomId + '.3')
            }
        }
    }
}
</script>

<style scoped>
.code-editor {
    width: 100%;
    height: auto;
}
</style>
