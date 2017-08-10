<template>
    <div class="code-editor">
        <Select v-model='editorOptions.mode' placeholder="language">
            <option v-for='mode in modeList' value='mode.modeValue':key='mode.modeName'>{{mode.modeName}}</option>
        </Select>
        <codemirror v-model='code' :options='editorOptions' readonly="false"></codemirror>
        <button @click="linshi">code<button>
    </div>
</template>


<script src="/socket.io/socket.io.js"></script>
<script>
import * as io from 'socket.io-client'
export default {
    name: 'code-editor',
    created () {
        this.roomid = this.$route.params.id
    },
    data () {
        return {
            code: 'const a = 10   123456789',
            editorOptions: {
                tabSize: 4,
                mode: 'text/javascript',
                theme: 'base16-dark',
                lineNumbers: true,
                line: true,
                keyMap: "sublime",
                extraKeys: { "Ctrl": "autocomplete" },
                foldGutter: true,
                gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
                styleSelectedText: true,
                highlightSelectionMatches: { showToken: /\w/, annotateScrollbar: true },
            },
            socket: '',
            roomid: '',
            modeList:[
                {
                    modeName:'JavaScript',
                    modeValue:'text/javascript'
                },
                {
                    modeName:'C/C++',
                    modeValue:'text/x-c++src'
                },
                {
                    modeName:'C#',
                    modeValue:'text/x-csharp'
                },
                {
                    modeName:'Java',
                    modeValue:'text/x-java'
                },
                {
                    modeName:'PHP',
                    modeValue:'application/x-httpd-php'
                },
            ]
        }
    },
    methods: {
    },
    mounted () {
        this.socket = io.connect('http://localhost:9000')
        this.socket.emit('join', this.roomid+'.3')
        var self = this
        this.socket.on('message', function (mes) {
            self.code = mes
        })
    },
    watch: {
        code: function (newcode, oldcode) {
            if(newcode !== oldcode) {
                this.socket.emit('message', newcode, this.roomid+'.3')
            }
        }
    }
}
</script>

<style scoped>
.code-editor {
	width: 670px;
	height: 450px;
}
</style>
