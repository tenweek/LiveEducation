<template>
    <div class="white-board">
        <div class="tools">
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
            <canvas ref="board" id="canvas" :width="teachingToolsWidth" :height="teachingToolsHeight"></canvas>
        </div>
    </div>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
/**
 * 实现教学区白板功能，
 * 作为子组件插入直播间页面。
 * 老师端可以对白板进行操作，
 * 可以选择画笔、直线、几何图形等进行画图，
 * 有填充、大小选择、橡皮擦、撤销等功能。
 * 学生端不能对白板操作，
 * 只能同步看到老师的操作。
 *
 * @module WhiteBoard
 * @class WhiteBoard
 */
import * as io from 'socket.io-client'
import myMsg from './../warning.js'
const MIN = 0.005
export default {
    name: 'white-board',
    props: ['roomId', 'teacherName', 'username', 'teachingToolsWidth', 'teachingToolsHeight'],
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
        /**
         * 初始化数据，在mounted中调用
         *
         * @method initData
         */
        initData: function () {
            this.context = this.$refs.board.getContext('2d')
            this.canvas = document.getElementById('canvas')
            this.canvas.style.cursor = 'default'
            this.allDataUrl.push(this.canvas.toDataURL())
            this.socket = io.connect('http://localhost:9000')
            this.socket.emit('joinForWhiteBoard', this.roomId + '.0')
        },
        /**
         * 当选择功能为橡皮擦且size值变化时调用，
         * 根据size的值改变橡皮擦光标的样式
         *
         * @method changeEraserCursor
         */
        changeEraserCursor: function () {
            if (this.size === 1) {
                this.canvas.style.cursor = "url('http://localhost:8000/static/eraserSmall.png'), default"
            } else if (this.size === 3) {
                this.canvas.style.cursor = "url('http://localhost:8000/static/eraserMiddle.png'), default"
            } else {
                this.canvas.style.cursor = "url('http://localhost:8000/static/eraserLarge.png'), default"
            }
        },
        /**
         * 将用户输入到文本输入框中的文字画到白板上，
         * 并且可以根据白板大小自动换行
         *
         * @method drawLongText
         * @param text 用户输入的文字
         * @param beginX 输入文字坐标点的横坐标
         * @param beginY 输入文字坐标点的纵坐标
         */
        drawLongText: function (text, beginX, beginY) {
            let textLength = text.length
            let rowLength = this.teachingToolsWidth - beginX
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
        /**
         * 用户（创建房间的老师）点击粗细
         */
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
                x: x / this.teachingToolsWidth,
                y: y / this.teachingToolsHeight,
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
                    x: x / this.teachingToolsWidth,
                    y: y / this.teachingToolsHeight,
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
                x: x / this.teachingToolsWidth,
                y: y / this.teachingToolsHeight,
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
                x: x / this.teachingToolsWidth,
                y: y / this.teachingToolsHeight,
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
                x: x / this.teachingToolsWidth,
                y: y / this.teachingToolsHeight,
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
                x: x / this.teachingToolsWidth,
                y: y / this.teachingToolsHeight,
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
                x: x / this.teachingToolsWidth,
                y: y / this.teachingToolsHeight,
                buttons: buttons,
                colorBorder: this.colorBorder,
                colorFill: this.colorFill,
                fill: this.fill
            }, this.roomId + '.0')
        },
        pen: function (data) {
            this.colorBorder = data.color
            if (data.action === 'mousedown') {
                this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
                this.lastImageData = this.context.getImageData(0, 0, this.teachingToolsWidth, this.teachingToolsHeight)
            } else if (data.action === 'mousemove') {
                this.penMousemove(data)
            } else if (data.action === 'mouseup') {
                this.originPoint = null
                this.lastImageData = null
                this.pointer += 1
                this.allDataUrl.push(this.canvas.toDataURL())
            }
        },
        penMousemove: function (data) {
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
            context.lineTo(data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight)
            context.stroke()
            context.closePath()
            this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
        },
        eraser: function (data) {
            switch (data.action) {
                case 'mousedown':
                    this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
                    this.lastImageData = this.context.getImageData(0, 0, this.teachingToolsWidth, this.teachingToolsHeight)
                    break
                case 'mousemove':
                    this.eraserMousemove(data)
                    break
                case 'mouseup':
                    this.originPoint = null
                    this.lastImageData = null
                    this.allDataUrl.push(this.canvas.toDataURL())
                    this.pointer += 1
                    break
            }
        },
        eraserMousemove: function (data) {
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
            this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
        },
        line: function (data) {
            this.colorBorder = data.color
            switch (data.action) {
                case 'mousedown':
                    this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
                    this.lastImageData = this.context.getImageData(0, 0, this.teachingToolsWidth, this.teachingToolsHeight)
                    break
                case 'mousemove':
                    this.lineMousemove(data)
                    break
                case 'mouseup':
                    this.originPoint = null
                    this.lastImageData = null
                    this.allDataUrl.push(this.canvas.toDataURL())
                    this.pointer += 1
                    break
            }
        },
        lineMousemove: function (data) {
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
            context.lineTo(data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight)
            context.stroke()
            context.closePath()
        },
        rectangle: function (data) {
            this.colorBorder = data.colorBorder
            this.colorFill = data.colorFill
            this.fill = data.fill
            switch (data.action) {
                case 'mousedown':
                    this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
                    this.lastImageData = this.context.getImageData(0, 0, this.teachingToolsWidth, this.teachingToolsHeight)
                    break
                case 'mousemove':
                    this.rectangleMousemove(data)
                    break
                case 'mouseup':
                    this.originPoint = null
                    this.lastImageData = null
                    this.allDataUrl.push(this.canvas.toDataURL())
                    this.pointer += 1
                    break
            }
        },
        rectangleMousemove: function (data) {
            // TODO:拆分函数
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
            const [dx, dy] = [data.x * this.teachingToolsWidth - ox, data.y * this.teachingToolsHeight - oy]
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
        },
        circle: function (data) {
            this.colorBorder = data.colorBorder
            this.colorFill = data.colorFill
            this.fill = data.fill
            switch (data.action) {
                case 'mousedown':
                    this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
                    this.lastImageData = this.context.getImageData(0, 0, this.teachingToolsWidth, this.teachingToolsHeight)
                    break
                case 'mousemove':
                    this.circleMousemove(data)
                    break
                case 'mouseup':
                    this.originPoint = null
                    this.lastImageData = null
                    this.allDataUrl.push(this.canvas.toDataURL())
                    this.pointer += 1
                    break
            }
        },
        circleMousemove: function (data) {
            // TODO:拆分函数
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
            const [dx, dy] = [data.x * this.teachingToolsWidth - ox, data.y * this.teachingToolsHeight - oy]
            const radius = Math.sqrt(dx * dx, dy * dy)
            context.lineWidth = this.size
            context.beginPath()
            context.arc((ox + data.x * this.teachingToolsWidth) / 2, (data.y * this.teachingToolsHeight + oy) / 2, radius, 0, 2 * Math.PI)
            if (this.fill === true) {
                context.fillStyle = this.colorFill
                context.fill()
            }
            if (this.border === true) {
                context.strokeStyle = this.colorBorder
                context.stroke()
            }
            context.closePath()
        },
        ellipse: function (data) {
            this.colorBorder = data.colorBorder
            this.colorFill = data.colorFill
            this.fill = data.fill
            switch (data.action) {
                case 'mousedown':
                    this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
                    this.lastImageData = this.context.getImageData(0, 0, this.teachingToolsWidth, this.teachingToolsHeight)
                    break
                case 'mousemove':
                    this.ellipseMousemove(data)
                    break
                case 'mouseup':
                    this.originPoint = null
                    this.lastImageData = null
                    this.allDataUrl.push(this.canvas.toDataURL())
                    this.pointer += 1
                    break
            }
        },
        ellipseMousemove: function (data) {
            // TODO:拆分函数
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
            const [dx, dy] = [Math.abs(data.x * this.teachingToolsWidth - ox), Math.abs(data.y * this.teachingToolsHeight - oy)]
            context.strokeStyle = this.colorBorder
            context.lineWidth = this.size
            if (this.fill === true) {
                context.fillStyle = this.colorFill
            }
            context.beginPath()
            context.ellipse((data.x * this.teachingToolsWidth + ox) / 2, (data.y * this.teachingToolsHeight + oy) / 2, dx / 2, dy / 2, 0, 0, 2 * Math.PI)
            if (this.fill === true) {
                context.fillStyle = this.colorFill
                context.fill()
            }
            if (this.border === true) {
                context.strokeStyle = this.colorBorder
                context.stroke()
            }
            context.closePath()
        },
        boardClear: function (data) {
            this.context.clearRect(0, 0, this.teachingToolsWidth, this.teachingToolsHeight)
            this.allDataUrl = []
            this.allDataUrl.push(this.canvas.toDataURL())
            this.pointer = 0
        },
        textBox: function (data) {
            if (data.action === 'mouseup') {
                this.textLeft = data.x * this.teachingToolsWidth
                this.textTop = data.y * this.teachingToolsHeight
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
                this.context.clearRect(0, 0, this.teachingToolsWidth, this.teachingToolsHeight)
                this.drawDataUrl(this.allDataUrl[this.pointer])
                this.allDataUrl.length = this.pointer + 1
            }
        },
        whiteBoardDoing: function (data) {
            if (data.type === 'pen') {
                this.pen(data)
            } else if (data.type === 'eraser') {
                this.eraser(data)
            } else if (data.type === 'line') {
                this.line(data)
            } else if (data.type === 'rectangle') {
                this.rectangle(data)
            } else if (data.type === 'circle') {
                this.circle(data)
            } else if (data.type === 'ellipse') {
                this.ellipse(data)
            } else if (data.type === 'clear') {
                this.clear(data)
            } else if (data.type === 'textField') {
                this.textBox(data)
            } else if (data.type === 'drawText') {
                this.font(data)
            } else if (data.type === 'undo') {
                this.boardUndo(data)
            }
        },
        buttonDoing: function (data) {
            if (data.type === 'eraser') {
                this.type = 'eraser'
            } else if (data.type === 'pen') {
                this.type = 'pen'
            } else if (data.type === 'text') {
                this.type = 'text'
            } else if (data.type === 'line') {
                this.type = 'line'
            } else if (data.type === 'rectangle') {
                this.type = 'rectangle'
            } else if (data.type === 'circle') {
                this.type = 'circle'
            } else if (data.type === 'ellipse') {
                this.type = 'ellipse'
            } else if (data.type === 'border') {
                this.border = !this.border
            } else if (data.type === 'fill') {
                this.fill = !this.fill
            } else if (data.type === 'sizeLarge') {
                this.size = 5
            } else if (data.type === 'sizeMiddle') {
                this.size = 3
            } else if (data.type === 'sizeSmall') {
                this.size = 1
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
                that.context.drawImage(img, 0, 0, that.teachingToolsWidth, that.teachingToolsHeight)
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

.tools {
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
