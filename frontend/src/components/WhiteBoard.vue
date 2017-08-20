<template>
    <div class="white-board">
        <div id="tools">
            <Button type="text" @click="clear">清空</Button>
            <Button type="text" @click="undo">撤销</Button>
            <Button type="text" :class="{ active: type === 'eraser' }" @click="clickEraser">橡皮擦</Button>
            <Button type="text" :class="{ active: type === 'pen' }" @click="clickPen">画笔</Button>
            <Button type="text" :class="{ active: type === 'text' }" @click="clickText">文字</Button>
            <Button type="text" :class="{ active: type === 'line' }" @click="clickLine">直线</Button>
            <Button type="text" :class="{ active: type === 'rectangle' }" @click="clickRectangle">矩形</Button>
            <Button type="text" :class="{ active: type === 'circle' }" @click="clickCircle">圆形</Button>
            <Button type="text" :class="{ active: type === 'ellipse' }" @click="clickEllipse">椭圆</Button>
            <Dropdown class="change-size" placement="right-start" @on-click="changeSize">
                <Button type="text">
                    粗细
                    <Icon type="ios-arrow-forward"></Icon>
                </Button>
                <Dropdown-menu slot="list" v-if="this.teacherName === this.username">
                    <Dropdown-item name='small'>小</Dropdown-item>
                    </Dropdown-item>
                    <Dropdown-item name='middle'>中</Dropdown-item>
                    <Dropdown-item name='large'>大</Dropdown-item>
                </Dropdown-menu>
            </Dropdown>
            <Button type="text" :class="{ active: border === true }" @click="clickBorder">边框</Button>
            <Button type="text" :class="{ active: fill === true }" @click="clickFill">填充</Button>
            <el-color-picker v-if="this.teacherName === this.username" class="color-selected" v-model="colorBorder" show-alpha></el-color-picker>
            <el-color-picker v-if="this.teacherName === this.username" class="color-selected" v-model="colorFill" show-alpha></el-color-picker>
        </div>
        <div class="drawing-board">
            <input id="text-field" @keyup.enter="drawText" v-show="this.textField === true" v-model="textInput" placeholder="请输入..." autofocus="true"></input>
            <canvas ref="board" id="canvas" :width="whiteBoardWidth" :height="whiteBoardHeight"></canvas>
        </div>
    </div>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
import * as io from 'socket.io-client'
import myMsg from './../warning.js'
const MIN = 0.005
export default {
    name: 'white-board',
    props: ['roomId', 'teacherName', 'username', 'whiteBoardWidth', 'whiteBoardHeight', 'isOnLeft'],
    data: function () {
        return {
            type: 'pen',
            context: null,
            originPoint: null,
            lastImageData: null,
            colorBorder: 'rgba(0, 0, 0, 1)',
            colorFill: 'rgba(255, 255, 255, 1)',
            fill: false,
            border: true,
            size: 1,
            textField: false,
            textInput: '',
            textLeft: 0,
            textTop: 0,
            canvas: null,
            allDataUrl: [],
            currentImageData: null,
            pointer: 0,
            socket: '',
            roomId: '',
            started: false
        }
    },
    watch: {
        type: function () {
            if (this.type === 'eraser') {
                this.changeEraserCursor()
            } else if (this.type === 'pen') {
                this.canvas.style.cursor = 'default'
            } else {
                this.canvas.style.cursor = 'crosshair'
            }
        },
        size: function () {
            if (this.type === 'eraser') {
                this.changeEraserCursor()
            }
        },
        whiteBoardWidth: function (newVal, oldVal) {
            document.getElementById('canvas').width = (newVal - 119) + 'px'
            console.log('whiteBoardWidth changed' + this.whiteBoardWidth)
        },
        whiteBoardHeight: function (newVal, oldVal) {
            document.getElementById('canvas').height = (newVal - 66) + 'px'
            console.log('whiteBoardHeight changed' + this.whiteBoardHeight)
        },
        isOnLeft: function (newVal, oldVal) {
            console.log('xx')
            if (newVal) {
                document.getElementById('tools').style.display = 'inline-block'
                console.log('ss')
            } else {
                document.getElementById('tools').style.display = 'none'
                console.log('bb')
            }
        }
    },
    mounted: function () {
        ['mousemove', 'mousedown', 'mouseup'].map((eventName) => {
            this.$refs.board.addEventListener(eventName, ({ offsetX: x, offsetY: y, buttons }) => {
                this[`${this.type}Command`](eventName, { x, y, buttons })
            })
        })
        this.initData()
        let self = this
        self.socket.on('message', function (data) {
            if (self.started === false) {
                return
            }
            self.whiteBoardDoing(data)
        })
        self.socket.on('click', function (data) {
            if (self.started === false) {
                return
            }
            self.buttonDoing(data)
        })
        self.socket.on('newJoin', function () {
            self.joinDoing()
        })
        self.socket.on('updateWhiteBoardMessage', function (data) {
            self.updateMessageDoing(data)
        })
        self.socket.on('getStarted', function () {
            self.started = true
        })
    },
    methods: {
        initData: function () {
            this.context = this.$refs.board.getContext('2d')
            this.canvas = document.getElementById('canvas')
            this.canvas.style.cursor = 'default'
            this.allDataUrl.push(this.canvas.toDataURL())
            this.socket = io.connect('http://localhost:9000')
            this.socket.emit('joinForWhiteBoard', this.roomId + '.0')
        },
        changeEraserCursor: function () {
            if (this.size === 1) {
                this.canvas.style.cursor = "url('http://localhost:8000/static/eraserSmall.png'), default"
            } else if (this.size === 3) {
                this.canvas.style.cursor = "url('http://localhost:8000/static/eraserMiddle.png'), default"
            } else {
                this.canvas.style.cursor = "url('http://localhost:8000/static/eraserLarge.png'), default"
            }
        },
        drawLongText: function (text, beginX, beginY) {
            let textLength = text.length
            let rowLength = this.whiteBoardWidth - beginX
            let newText = text.split('')
            let rowText = ''
            let count = 0
            this.context.textAlign = 'left'
            for (let i = 0; i <= textLength; i++) {
                if (i === textLength) {
                    this.context.fillText(rowText, beginX, beginY)
                }
                if (count <= rowLength && (count + this.context.measureText(newText[0]).width > rowLength)) {
                    this.context.fillText(rowText, beginX, beginY)
                    beginY = beginY + this.size * 5 + 28
                    rowText = ''
                    count = 0
                }
                rowText = rowText + newText[0]
                count += this.context.measureText(newText[0]).width
                newText.shift()
            }
        },
        changeSize: function (name) {
            if (this.teacherName !== this.username) {
                return
            }
            if (name === 'large') {
                this.socket.emit('click', { type: 'sizeLarge' }, this.roomId + '.0')
            } else if (name === 'middle') {
                this.socket.emit('click', { type: 'sizeMiddle' }, this.roomId + '.0')
            } else {
                this.socket.emit('click', { type: 'sizeSmall' }, this.roomId + '.0')
            }
        },
        clickEraser: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'eraser' }, this.roomId + '.0')
        },
        clickPen: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'pen' }, this.roomId + '.0')
        },
        clickText: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'text' }, this.roomId + '.0')
        },
        clickLine: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'line' }, this.roomId + '.0')
        },
        clickRectangle: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'rectangle' }, this.roomId + '.0')
        },
        clickCircle: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'circle' }, this.roomId + '.0')
        },
        clickEllipse: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'ellipse' }, this.roomId + '.0')
        },
        clickBorder: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'border' }, this.roomId + '.0')
        },
        clickFill: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'fill' }, this.roomId + '.0')
        },
        drawText: function () {
            if (this.teacherName !== this.username) {
                return
            }
            let input = this.textInput
            this.socket.emit('message', {
                type: 'drawText',
                input: input
            }, this.roomId + '.0')
        },
        clear: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('message', { type: 'clear' }, this.roomId + '.0')
        },
        undo: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('message', { type: 'undo' }, this.roomId + '.0')
        },
        penCommand: function (action, { x, y, buttons }) {
            if (this.teacherName !== this.username) {
                return
            }
            if (action === 'mousemove' && this.originPoint === null) {
                return
            }
            this.socket.emit('message', {
                type: 'pen',
                action: action,
                x: x / this.whiteBoardWidth,
                y: y / this.whiteBoardHeight,
                buttons: buttons,
                color: this.colorBorder
            }, this.roomId + '.0')
        },
        textCommand: function (action, { x, y, buttons }) {
            if (this.teacherName !== this.username) {
                return
            }
            if (action === 'mouseup') {
                this.textField = true
                let textField = document.getElementById('text-field')
                textField.style.autofocus = 'true'
                this.socket.emit('message', {
                    type: 'textField',
                    x: x / this.whiteBoardWidth,
                    y: y / this.whiteBoardHeight,
                    color: this.colorBorder,
                    action: action,
                    buttons: buttons
                }, this.roomId + '.0')
            }
        },
        eraserCommand: function (action, { x, y, buttons }) {
            if (this.teacherName !== this.username) {
                return
            }
            if (action === 'mousemove' && this.originPoint === null) {
                return
            }
            this.socket.emit('message', {
                type: 'eraser',
                action: action,
                x: x / this.whiteBoardWidth,
                y: y / this.whiteBoardHeight,
                buttons: buttons
            }, this.roomId + '.0')
        },
        lineCommand: function (action, { x, y, buttons }) {
            if (this.teacherName !== this.username) {
                return
            }
            if (action === 'mousemove' && this.originPoint === null) {
                return
            }
            this.socket.emit('message', {
                type: 'line',
                action: action,
                x: x / this.whiteBoardWidth,
                y: y / this.whiteBoardHeight,
                buttons: buttons,
                color: this.colorBorder
            }, this.roomId + '.0')
        },
        rectangleCommand: function (action, { x, y, buttons }) {
            if (this.teacherName !== this.username) {
                return
            }
            if (action === 'mousemove' && this.originPoint === null) {
                return
            }
            this.socket.emit('message', {
                type: 'rectangle',
                action: action,
                x: x / this.whiteBoardWidth,
                y: y / this.whiteBoardHeight,
                buttons: buttons,
                colorBorder: this.colorBorder,
                colorFill: this.colorFill,
                fill: this.fill
            }, this.roomId + '.0')
        },
        circleCommand: function (action, { x, y, buttons }) {
            if (this.teacherName !== this.username) {
                return
            }
            if (action === 'mousemove' && this.originPoint === null) {
                return
            }
            this.socket.emit('message', {
                type: 'circle',
                action: action,
                x: x / this.whiteBoardWidth,
                y: y / this.whiteBoardHeight,
                buttons: buttons,
                colorBorder: this.colorBorder,
                colorFill: this.colorFill,
                fill: this.fill
            }, this.roomId + '.0')
        },
        ellipseCommand: function (action, { x, y, buttons }) {
            if (this.teacherName !== this.username) {
                return
            }
            if (action === 'mousemove' && this.originPoint === null) {
                return
            }
            this.socket.emit('message', {
                type: 'ellipse',
                action: action,
                x: x / this.whiteBoardWidth,
                y: y / this.whiteBoardHeight,
                buttons: buttons,
                colorBorder: this.colorBorder,
                colorFill: this.colorFill,
                fill: this.fill
            }, this.roomId + '.0')
        },
        pen: function (data) {
            this.colorBorder = data.color
            if (data.action === 'mousedown') {
                this.originPoint = [data.x * this.whiteBoardWidth, data.y * this.whiteBoardHeight]
                this.lastImageData = this.context.getImageData(0, 0, this.whiteBoardWidth, this.whiteBoardHeight)
            } else if (data.action === 'mousemove') {
                if (this.originPoint === null) {
                    return
                }
                if (data.x < MIN || data.x > (1 - MIN) || data.y < MIN || data.y > (1 - MIN)) {
                    this.originPoint = null
                    this.lastImageData = null
                    this.pointer += 1
                    this.allDataUrl.push(this.canvas.toDataURL())
                    return
                }
                const context = this.context
                const [ox, oy] = this.originPoint
                context.strokeStyle = this.colorBorder
                context.lineWidth = this.size
                context.beginPath()
                context.moveTo(ox, oy)
                context.lineTo(data.x * this.whiteBoardWidth, data.y * this.whiteBoardHeight)
                context.stroke()
                context.closePath()
                this.originPoint = [data.x * this.whiteBoardWidth, data.y * this.whiteBoardHeight]
            } else if (data.action === 'mouseup') {
                this.originPoint = null
                this.lastImageData = null
                this.pointer += 1
                this.allDataUrl.push(this.canvas.toDataURL())
            }
        },
        eraser: function (data) {
            switch (data.action) {
                case 'mousedown':
                    this.originPoint = [data.x * this.whiteBoardWidth, data.y * this.whiteBoardHeight]
                    this.lastImageData = this.context.getImageData(0, 0, this.whiteBoardWidth, this.whiteBoardHeight)
                    break
                case 'mousemove':
                    if (this.originPoint === null) {
                        return
                    }
                    if (data.x < MIN || data.x > (1 - MIN) || data.y < MIN || data.y > (1 - MIN)) {
                        this.originPoint = null
                        this.lastImageData = null
                        this.allDataUrl.push(this.canvas.toDataURL())
                        this.pointer += 1
                        return
                    }
                    const context = this.context
                    const [ox, oy] = this.originPoint
                    context.clearRect(ox, oy, this.size * 10, this.size * 10)
                    this.originPoint = [data.x * this.whiteBoardWidth, data.y * this.whiteBoardHeight]
                    break
                case 'mouseup':
                    this.originPoint = null
                    this.lastImageData = null
                    this.allDataUrl.push(this.canvas.toDataURL())
                    this.pointer += 1
                    break
            }
        },
        line: function (data) {
            this.colorBorder = data.color
            switch (data.action) {
                case 'mousedown':
                    this.originPoint = [data.x * this.whiteBoardWidth, data.y * this.whiteBoardHeight]
                    this.lastImageData = this.context.getImageData(0, 0, this.whiteBoardWidth, this.whiteBoardHeight)
                    break
                case 'mousemove':
                    if (this.originPoint == null) {
                        return
                    }
                    if (data.x < MIN || data.x > (1 - MIN) || data.y < MIN || data.y > (1 - MIN)) {
                        this.originPoint = null
                        this.lastImageData = null
                        this.allDataUrl.push(this.canvas.toDataURL())
                        this.pointer += 1
                        return
                    }
                    const context = this.context
                    context.putImageData(this.lastImageData, 0, 0)
                    const [ox, oy] = this.originPoint
                    context.strokeStyle = this.colorBorder
                    context.lineWidth = this.size
                    context.beginPath()
                    context.moveTo(ox, oy)
                    context.lineTo(data.x * this.whiteBoardWidth, data.y * this.whiteBoardHeight)
                    context.stroke()
                    context.closePath()
                    break
                case 'mouseup':
                    this.originPoint = null
                    this.lastImageData = null
                    this.allDataUrl.push(this.canvas.toDataURL())
                    this.pointer += 1
                    break
            }
        },
        rectangle: function (data) {
            this.colorBorder = data.colorBorder
            this.colorFill = data.colorFill
            this.fill = data.fill
            switch (data.action) {
                case 'mousedown':
                    this.originPoint = [data.x * this.whiteBoardWidth, data.y * this.whiteBoardHeight]
                    this.lastImageData = this.context.getImageData(0, 0, this.whiteBoardWidth, this.whiteBoardHeight)
                    break
                case 'mousemove':
                    if (this.originPoint === null) {
                        return
                    }
                    if (data.x < MIN || data.x > (1 - MIN) || data.y < MIN || data.y > (1 - MIN)) {
                        this.originPoint = null
                        this.lastImageData = null
                        this.allDataUrl.push(this.canvas.toDataURL())
                        this.pointer += 1
                        return
                    }
                    const context = this.context
                    context.putImageData(this.lastImageData, 0, 0)
                    const [ox, oy] = this.originPoint
                    const [dx, dy] = [data.x * this.whiteBoardWidth - ox, data.y * this.whiteBoardHeight - oy]
                    context.lineWidth = this.size
                    context.beginPath()
                    context.rect(ox, oy, dx, dy)
                    if (this.fill === true) {
                        context.fillStyle = this.colorFill
                        context.fill()
                    }
                    if (this.border === true) {
                        context.strokeStyle = this.colorBorder
                        context.stroke()
                    }
                    context.closePath()
                    break
                case 'mouseup':
                    this.originPoint = null
                    this.lastImageData = null
                    this.allDataUrl.push(this.canvas.toDataURL())
                    this.pointer += 1
                    break
            }
        },
        circle: function (data) {
            this.colorBorder = data.colorBorder
            this.colorFill = data.colorFill
            this.fill = data.fill
            switch (data.action) {
                case 'mousedown':
                    this.originPoint = [data.x * this.whiteBoardWidth, data.y * this.whiteBoardHeight]
                    this.lastImageData = this.context.getImageData(0, 0, this.whiteBoardWidth, this.whiteBoardHeight)
                    break
                case 'mousemove':
                    if (this.originPoint === null) {
                        return
                    }
                    if (data.x < MIN || data.x > (1 - MIN) || data.y < MIN || data.y > (1 - MIN)) {
                        this.originPoint = null
                        this.lastImageData = null
                        this.allDataUrl.push(this.canvas.toDataURL())
                        this.pointer += 1
                        return
                    }
                    const context = this.context
                    context.putImageData(this.lastImageData, 0, 0)
                    const [ox, oy] = this.originPoint
                    const [dx, dy] = [data.x * this.whiteBoardWidth - ox, data.y * this.whiteBoardHeight - oy]
                    const radius = Math.sqrt(dx * dx, dy * dy)
                    context.lineWidth = this.size
                    context.beginPath()
                    context.arc((ox + data.x * this.whiteBoardWidth) / 2, (data.y * this.whiteBoardHeight + oy) / 2, radius, 0, 2 * Math.PI)
                    if (this.fill === true) {
                        context.fillStyle = this.colorFill
                        context.fill()
                    }
                    if (this.border === true) {
                        context.strokeStyle = this.colorBorder
                        context.stroke()
                    }
                    context.closePath()
                    break
                case 'mouseup':
                    this.originPoint = null
                    this.lastImageData = null
                    this.allDataUrl.push(this.canvas.toDataURL())
                    this.pointer += 1
                    break
            }
        },
        ellipse: function (data) {
            this.colorBorder = data.colorBorder
            this.colorFill = data.colorFill
            this.fill = data.fill
            switch (data.action) {
                case 'mousedown':
                    this.originPoint = [data.x * this.whiteBoardWidth, data.y * this.whiteBoardHeight]
                    this.lastImageData = this.context.getImageData(0, 0, this.whiteBoardWidth, this.whiteBoardHeight)
                    break
                case 'mousemove':
                    if (this.originPoint === null) {
                        return
                    }
                    if (data.x < MIN || data.x > (1 - MIN) || data.y < MIN || data.y > (1 - MIN)) {
                        this.originPoint = null
                        this.lastImageData = null
                        this.allDataUrl.push(this.canvas.toDataURL())
                        this.pointer += 1
                        return
                    }
                    const context = this.context
                    context.putImageData(this.lastImageData, 0, 0)
                    const [ox, oy] = this.originPoint
                    const [dx, dy] = [Math.abs(data.x * this.whiteBoardWidth - ox), Math.abs(data.y * this.whiteBoardHeight - oy)]
                    context.strokeStyle = this.colorBorder
                    context.lineWidth = this.size
                    if (this.fill === true) {
                        context.fillStyle = this.colorFill
                    }
                    context.beginPath()
                    context.ellipse((data.x * this.whiteBoardWidth + ox) / 2, (data.y * this.whiteBoardHeight + oy) / 2, dx / 2, dy / 2, 0, 0, 2 * Math.PI)
                    if (this.fill === true) {
                        context.fillStyle = this.colorFill
                        context.fill()
                    }
                    if (this.border === true) {
                        context.strokeStyle = this.colorBorder
                        context.stroke()
                    }
                    context.closePath()
                    break
                case 'mouseup':
                    this.originPoint = null
                    this.lastImageData = null
                    this.allDataUrl.push(this.canvas.toDataURL())
                    this.pointer += 1
                    break
            }
        },
        boardClear: function (data) {
            this.context.clearRect(0, 0, this.whiteBoardWidth, this.whiteBoardHeight)
            this.allDataUrl = []
            this.allDataUrl.push(this.canvas.toDataURL())
            this.pointer = 0
        },
        textBox: function (data) {
            if (data.action === 'mouseup') {
                this.textLeft = data.x * this.whiteBoardWidth
                this.textTop = data.y * this.whiteBoardHeight
                this.colorBorder = data.color
            }
        },
        font: function (data) {
            this.textField = false
            this.context.font = (this.size * 5 + 25) + 'px serif'
            this.context.fillStyle = this.colorBorder
            this.drawLongText(data.input, this.textLeft, this.textTop)
            this.textInput = ''
            this.allDataUrl.push(this.canvas.toDataURL())
            this.pointer += 1
        },
        boardUndo: function (data) {
            if (this.started === false) {
                return
            }
            if (this.pointer === 0) {
                this.$Message.error(myMsg.whiteBoard['undoNotExist'])
                return
            } else {
                this.pointer -= 1
                this.context.clearRect(0, 0, this.whiteBoardWidth, this.whiteBoardHeight)
                this.drawDataUrl(this.allDataUrl[this.pointer])
                this.allDataUrl.length = this.pointer + 1
            }
        },
        whiteBoardDoing: function (data) {
            switch (data.type) {
                case 'pen':
                    this.pen(data)
                    break
                case 'eraser':
                    this.eraser(data)
                    break
                case 'line':
                    this.line(data)
                    break
                case 'rectangle':
                    this.rectangle(data)
                    break
                case 'circle':
                    this.circle(data)
                    break
                case 'ellipse':
                    this.ellipse(data)
                    break
                case 'clear':
                    this.boardClear(data)
                    break
                case 'textField':
                    this.textBox(data)
                    break
                case 'drawText':
                    this.font(data)
                    break
                case 'undo':
                    this.boardUndo(data)
                    break
            }
        },
        buttonDoing: function (data) {
            switch (data.type) {
                case 'eraser':
                    this.type = 'eraser'
                    break
                case 'pen':
                    this.type = 'pen'
                    break
                case 'text':
                    this.type = 'text'
                    break
                case 'line':
                    this.type = 'line'
                    break
                case 'rectangle':
                    this.type = 'rectangle'
                    break
                case 'circle':
                    this.type = 'circle'
                    break
                case 'ellipse':
                    this.type = 'ellipse'
                    break
                case 'border':
                    this.border = !this.border
                    break
                case 'fill':
                    this.fill = !this.fill
                    break
                case 'sizeLarge':
                    this.size = 5
                    break
                case 'sizeMiddle':
                    this.size = 3
                    break
                case 'sizeSmall':
                    this.size = 1
                    break
            }
        },
        joinDoing: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('newJoinWhiteBoardMessage', {
                type: this.type,
                border: this.border,
                fill: this.fill,
                size: this.size,
                dataUrl: this.allDataUrl
            }, this.roomId + '.0')
        },
        updateMessageDoing: function (data) {
            if (this.teacherName !== this.username) {
                this.allDataUrl = data.dataUrl
                this.type = data.type
                this.border = this.border
                this.fill = data.fill
                this.size = data.size
                this.pointer = this.allDataUrl.length - 1
                this.drawDataUrl(this.allDataUrl[this.pointer])
            }
        },
        drawDataUrl: function (dataUrl) {
            let img = new Image()
            let that = this
            img.onload = function () {
                that.context.drawImage(img, 0, 0, that.whiteBoardWidth, that.whiteBoardHeight)
            }
            img.src = dataUrl
        }
    }
}
</script>

<style scoped>
#text-field {
    position: absolute;
    width: 300px;
}

.white-board {
    height: 100%;
    display: flex;
    cursor: hand;
}

#tools {
    height: auto;
    width: 85px;
    background: #efefef;
}

button {
    background-color: #efefef;
    height: 30px;
    width: 74px;
    margin-left: 0;
    margin-right: 0;
}

button.active {
    background-color: #aaa;
}

.color-selected {
    margin-left: 8px;
}

.drawing-board {
    height: 100%;
    width: 100%;
}
</style>
