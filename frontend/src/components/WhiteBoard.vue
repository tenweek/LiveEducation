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
/**
 * 用于判断鼠标在画图过程中是否移出canvas
 *
 * @attribute MIN
 * @readOnly
 * @default 0.005
 * @type Number
 */
const MIN = 0.005
export default {
    name: 'white-board',
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
     *表示正在观看直播的用户名字
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
    props: ['roomId', 'teacherName', 'username', 'teachingToolsWidth', 'teachingToolsHeight'],
    data: function () {
        return {
            /**
             * 表示当前老师选中的功能
             *
             * @attribute type
             * @type String
             * @default 'pen'
             */
            type: 'pen',
            /**
             * 用于表示
             */
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
         * 用户（创建房间的老师）点击粗细选择大小时触发，
         * 箱服务器发送click消息，data中包含"size"的信息
         *
         * @method changeSize
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
        /**
         * 用户（创建房间的老师）点击橡皮擦按钮时触发，
         * 向服务器发送click消息，data中包含"橡皮擦"信息
         *
         * @method clickEraser
         */
        clickEraser: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'eraser' }, this.roomId + '.0')
        },
        /**
         * 用户（创建房间的老师）点击画笔按钮时触发，
         * 向服务器发送click消息，data中包含"画笔"信息
         *
         * @method clickPen
         */
        clickPen: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'pen' }, this.roomId + '.0')
        },
        /**
         * 用户（创建房间的老师）点击文字按钮时触发，
         * 向服务器发送click消息，data中包含"文字"信息
         *
         * @method clickPen
         */
        clickText: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'text' }, this.roomId + '.0')
        },
        /**
         * 用户（创建房间的老师）点击直线按钮时触发，
         * 向服务器发送click消息，data中包含"直线"信息
         *
         * @method clickLine
         */
        clickLine: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'line' }, this.roomId + '.0')
        },
        /**
         * 用户（创建房间的老师）点击矩形按钮时触发，
         * 向服务器发送click消息，data中包含"矩形"信息
         *
         * @method clickRectangle
         */
        clickRectangle: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'rectangle' }, this.roomId + '.0')
        },
        /**
         * 用户（创建房间的老师）点击圆形按钮时触发，
         * 向服务器发送click消息，data中包含"圆形"信息
         *
         * @method clickCircle
         */
        clickCircle: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'circle' }, this.roomId + '.0')
        },
        /**
         * 用户（创建房间的老师）点击椭圆按钮时触发，
         * 向服务器发送click消息，data中包含"椭圆"信息
         *
         * @method clickEllipse
         */
        clickEllipse: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'ellipse' }, this.roomId + '.0')
        },
        /**
         * 用户（创建房间的老师）点击边框按钮时触发，
         * 向服务器发送click消息，data中包含"边框"信息
         *
         * @method clickBorder
         */
        clickBorder: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'border' }, this.roomId + '.0')
        },
        /**
         * 用户（创建房间的老师）点击填充按钮时触发，
         * 向服务器发送click消息，data中包含"填充"信息
         *
         * @method clickFill
         */
        clickFill: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('click', { type: 'fill' }, this.roomId + '.0')
        },
        /**
         * 用户（创建房间的老师）在文本框输入文字后按下回车键是响应，
         * 向服务器发送'message'消息，包含输入的文字信息
         *
         * @method drawText
         */
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
        /**
         * 用户（创建房间的老师）按下清空按钮时响应，
         * 向服务器发送'message'消息，包含"清空"信息
         *
         * @method clear
         */
        clear: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('message', { type: 'clear' }, this.roomId + '.0')
        },
        /**
         * 用户（创建房间的老师）按下撤销按钮时响应，
         * 向服务器发送'message'消息，包含"撤销"信息
         *
         * @method undo
         */
        undo: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('message', { type: 'undo' }, this.roomId + '.0')
        },
        /**
         * 用户（创建房间的老师）使用画笔功能对白板进行操作的时候响应，
         * 向服务器发送操作的数据
         *
         * @method penCommand
         * @param action 表示鼠标事件，包括mousedown、mousemove、mouseup
         * @param { x, y, buttons} 其中x、y表示当前鼠标在白板上的坐标
         */
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
        /**
         * 用户（创建房间的老师）使用文字功能对白板进行操作的时候响应，
         * 向服务器发送操作的数据（在mouseup的时候响应）
         *
         * @method textCommand
         * @param action 表示鼠标事件，包括mousedown、mousemove、mouseup
         * @param { x, y, buttons} 其中x、y表示当前鼠标在白板上的坐标
         */
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
        /**
         * 用户（创建房间的老师）使用橡皮擦功能对白板进行操作的时候响应，
         * 向服务器发送操作的数据
         *
         * @method eraserCommand
         * @param action 表示鼠标事件，包括mousedown、mousemove、mouseup
         * @param { x, y, buttons} 其中x、y表示当前鼠标在白板上的坐标
         */
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
        /**
         * 用户（创建房间的老师）使用直线功能对白板进行操作的时候响应，
         * 向服务器发送操作的数据
         *
         * @method lineCommand
         * @param action 表示鼠标事件，包括mousedown、mousemove、mouseup
         * @param { x, y, buttons} 其中x、y表示鼠标在白板上的坐标
         */
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
        /**
         * 用户（创建房间的老师）使用画矩形功能对白板进行操作的时候响应，
         * 向服务器发送操作的数据
         *
         * @method rectangleCommand
         * @param action 表示鼠标事件，包括mousedown、mousemove、mouseup
         * @param { x, y, buttons} 其中x、y表示鼠标在白板上的坐标
         */
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
        /**
         * 用户（创建房间的老师）使用画圆功能对白板进行操作的时候响应，
         * 向服务器发送操作的数据
         *
         * @method circleCommand
         * @param action 表示鼠标事件，包括mousedown、mousemove、mouseup
         * @param { x, y, buttons} 其中x、y表示鼠标在白板上的坐标
         */
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
        /**
         * 用户（创建房间的老师）使用画椭圆功能对白板进行操作的时候响应，
         * 向服务器发送操作的数据
         *
         * @method penCommand
         * @param action 表示鼠标事件，包括mousedown、mousemove、mouseup
         * @param { x, y, buttons} 其中x、y表示鼠标在白板上的坐标
         */
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
        /**
         * 根据接收到的信息对画板进行画笔操作
         *
         * @method pen
         * @param data 从服务器接收到的信息，包含对画板操作的数据
         */
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
        /**
         * 当从服务器接收到的信息是画笔操作，且鼠标事件为mousemove时调用。
         *
         * @method penMousemove
         * @param data 从服务器接收的信息，包括对画板进行操作的数据
         */
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
        /**
         * 根据接收到的信息对画板进行橡皮擦操作
         *
         * @method eraser
         * @param data 从服务器接收到的信息，包含对画板操作的数据
         */
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
        /**
         * 当从服务器接收到的信息是橡皮擦操作，且鼠标事件为mousemove时调用。
         *
         * @method eraserMousemove
         * @param data 从服务器接收的信息，包括对画板进行操作的数据
         */
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
        /**
         * 根据接收到的信息对画板进行直线操作
         *
         * @method line
         * @param data 从服务器接收到的信息，包含对画板操作的数据
         */
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
        /**
         * 当从服务器接收到的信息是直线操作，且鼠标事件为mousemove时调用。
         *
         * @method lineMousemove
         * @param data 从服务器接收的信息，包括对画板进行操作的数据
         */
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
        /**
         * 根据接收到的信息对画板进行画矩形操作
         *
         * @method rectangle
         * @param data 从服务器接收到的信息，包含对画板操作的数据
         */
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
        /**
         * 当从服务器接收到的信息是画矩形操作，且鼠标事件为mousemove时调用。
         *
         * @method rectangleMousemove
         * @param data 从服务器接收的信息，包括对画板进行操作的数据
         */
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
        /**
         * 根据接收到的信息对画板进行画圆形操作
         *
         * @method circle
         * @param data 从服务器接收到的信息，包含对画板操作的数据
         */
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
        /**
         * 当从服务器接收到的信息是画圆形操作，且鼠标事件为mousemove时调用。
         *
         * @method circleMousemove
         * @param data 从服务器接收的信息，包括对画板进行操作的数据
         */
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
        /**
         * 根据接收到的信息对画板进行画椭圆操作
         *
         * @method ellipse
         * @param data 从服务器接收到的信息，包含对画板操作的数据
         */
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
        /**
         * 当从服务器接收到的信息是画椭圆操作，且鼠标事件为mousemove时调用。
         *
         * @method ellipseMousemove
         * @param data 从服务器接收的信息，包括对画板进行操作的数据
         */
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
        /**
         * 在'whiteBoardDoing'函数中调用，
         * 接收到服务器消息后清空画板
         *
         * @method boardClear
         * @param data 从服务器接收到的数据，包含"清空"信息
         */
        boardClear: function (data) {
            this.context.clearRect(0, 0, this.teachingToolsWidth, this.teachingToolsHeight)
            this.allDataUrl = []
            this.allDataUrl.push(this.canvas.toDataURL())
            this.pointer = 0
        },
        /**
         * 在'whiteBoardDoing'函数中调用，
         * 根据服务器传来的信息更新自己的数据，
         * 同步到老师端。
         *
         * @method textBox
         * @param data 从服务器接收到的数据，包含文字坐标、颜色等信息
         */
        textBox: function (data) {
            if (data.action === 'mouseup') {
                this.textLeft = data.x * this.teachingToolsWidth
                this.textTop = data.y * this.teachingToolsHeight
                this.colorBorder = data.color
            }
        },
        /**
         * 在'whiteBoardDoing'函数中调用，
         * 将指定文本内容画到画板上
         *
         * @method font
         * @param data 从服务器接收到的数据，包含文本内容等信息
         */
        font: function (data) {
            this.textField = false
            this.context.font = (this.size * 5 + 25) + 'px serif'
            this.context.fillStyle = this.colorBorder
            this.drawLongText(data.input, this.textLeft, this.textTop)
            this.textInput = ''
            this.allDataUrl.push(this.canvas.toDataURL())
            this.pointer += 1
        },
        /**
         * 在'whiteBoardDoing'函数中调用，
         * 接收到服务器端的信息后，执行undo操作
         *
         * @method boardUndo
         */
        boardUndo: function () {
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
        /**
         * 当用户接收到'message'消息时，对画板进行绘图操作
         *
         * @method whiteBoardDoing
         * @param data 从服务器接收到的信息，包括在画板上操作的坐标、颜色、形状等信息
         */
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
                this.boardClear(data)
            } else if (data.type === 'textField') {
                this.textBox(data)
            } else if (data.type === 'drawText') {
                this.font(data)
            } else if (data.type === 'undo') {
                this.boardUndo()
            }
        },
        /**
         * 用户在开始直播后接收到'click'消息后，
         * 根据传输数据的类型，改变相应属性，完成点击按钮事件的响应。
         *
         * @method buttonDoing
         * @param data 从服务器端接收到的信息，包括点击的按钮类型
         */
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
        /**
         * 当用户（创建房间的老师）接收到'newJoin'消息时调用，
         * 老师直播过程中有新的用户进入房间，
         * 老师就把自己对白板操作的信息都发送到服务器，
         * 以达到学生同步的目的。
         *
         * @method joinDoing
         */
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
        /**
         * 当用户接收到'updateWhiteBoardMessage'消息时调用
         * （老师直播过程中有新的用户进入房间），
         * 将自己的信息同步到老师端
         *
         * @method updateMessageDoing
         * @param data 从服务器接收的信息，包括老师端对画板操作的所有信息
         */
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
        /**
         * 将指定dataURL画到canvas上
         *
         * @method drawDataUrl
         * @param dataUrl 将要画到canvas上的base64编码的图形对象
         */
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
