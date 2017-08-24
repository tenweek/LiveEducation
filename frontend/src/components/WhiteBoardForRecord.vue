<template>
    <div class="white-board">
        <div class="drawing-board">
            <canvas ref="board" id="canvas" :width="this.teachingToolsWidth" :height="this.teachingToolsHeight"></canvas>
        </div>
    </div>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
/**
 * 实现教学区白板的复现，
 * 作为子组件插入录播间页面，
 * 用户不能对白板操作。
 *
 * @module WhiteBoardForRecord
 * @class WhiteBoardForRecord
 */
import * as io from 'socket.io-client'
import myMsg from './../warning.js'
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
    props: ['roomId', 'userAccount', 'teachingToolsWidth', 'teachingToolsHeight'],
    data: function () {
        return {
            /**
             * 表示当前老师选中的绘图功能
             *
             * @attribute type
             * @type String
             * @default 'pen'
             */
            type: 'pen',
            /**
             * 获取canvas的上下文，指代页面上的绘图区域，
             * 用于对白板操作。
             *
             * @attribute context
             * @type null
             */
            /**
             * 表示绘图过程中（mousemove时）上一次鼠标的位置，
             * 在没有画图操作的时候为空。
             *
             * @attribute originPoint
             * @type null
             */
            originPoint: null,
            /**
             * 表示绘图过程中（mousemove时）上一次操作的绘图结果，
             * 在没有画图操作的时候为空。
             *
             * @attribute lastImageData
             * @type null
             */
            lastImageData: null,
            /**
             * 表示画板上边框的颜色（第一个颜色选择器）
             *
             * @attribute colorBorder
             * @type String
             * @default 'rgba(0, 0, 0, 1)'
             */
            colorBorder: 'rgba(0, 0, 0, 1)',
            /**
             * 表示画板上填充的颜色（第二个颜色选择器）
             *
             * @attribute colorFill
             * @type String
             * @default 'rgba(255, 255, 255, 1)'
             */
            colorFill: 'rgba(255, 255, 255, 1)',
            /**
             * 表示是否选择"填充"按钮
             *
             * @attribute fill
             * @type Boolean
             * @default false
             */
            fill: false,
            /**
             * 表示是否选择"边框"按钮
             *
             * @attribute border
             * @type Boolean
             * @default true
             */
            border: true,
            /**
             * 表示是否选择粗细的大小
             *
             * @attribute size
             * @type Number
             * @default 1
             */
            size: 1,
            /**
             * 表示文本输入框是否显示
             *
             * @attribute textField
             * @type Boolean
             * @default false
             */
            textField: false,
            /**
             * 表示文本输入框中输入的文字
             *
             * @attribute textInput
             * @type String
             * @default ''
             */
            textInput: '',
            /**
             * 表示绘制文字时文字起始位置的横坐标
             *
             * @attribute textLeft
             * @type Number
             * @default 0
             */
            textLeft: 0,
            /**
             * 表示绘制文字时文字起始位置的纵坐标
             *
             * @attribute textTop
             * @type Number
             * @default 0
             */
            textTop: 0,
            /**
             * 指向canvas画板对象
             *
             * @attribute canvas
             * @type null
             */
            canvas: null,
            /**
             * 存储画板上每次操作对应的图片
             *
             * @attribute allDataUrl
             * @type Array
             */
            allDataUrl: [],
            /**
             * 表示一个指针，指向allDataUrl中当前画板的状态，
             * 在undo操作时前移一个，从而实现undo操作。
             *
             * @attribute pointer
             * @type Number
             * @default 0
             */
            pointer: 0,
            /**
             * 表示客户端，监听服务器传来的消息
             *
             * @attribute socket
             * @type Object
             * @default ''
             */
            socket: ''
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
    /**
     * mounted函数，初始化数据，客户端监听服务器消息
     *
     * @method mounted
     */
    mounted: function () {
        this.initData()
        let self = this
        self.socket.on('whiteboard', function (data) {
            self.whiteBoardDoing(data)
        })
        self.socket.on('click', function (data) {
            self.buttonDoing(data)
        })
        self.socket.on('updateWhiteBoardMessage', function (data) {
            self.updateMessageDoing(data)
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
            this.socket.emit('joinTest', this.roomId, this.userAccount + 'w')
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
         * 将指定文字画到白板上，
         * 并且可以根据白板大小自动换行
         *
         * @method drawLongText
         * @param text 输入的文字
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
         * 判断绘图过程中鼠标是否移出canvas
         *
         * @method isOutCanvas
         * @param data
         * @return true表示鼠标移出canvas；false表示鼠标在canvas上
         */
        isOutCanvas: function (data) {
            if (data.x < MIN || data.x > (1 - MIN) || data.y < MIN || data.y > (1 - MIN)) {
                this.originPoint = null
                this.lastImageData = null
                this.allDataUrl.push(this.canvas.toDataURL())
                this.pointer += 1
                return true
            } else {
                return false
            }
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
            if (this.isOutCanvas(data) === true) {
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
            if (this.isOutCanvas(data) === true) {
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
            if (this.originPoint === null) {
                return
            }
            if (this.isOutCanvas(data) === true) {
                return
            }
            this.rectangleMousemoveDrawing(data)
        },
        /**
         * 绘制矩形，在rectangleMousemove函数中调用
         *
         * @method rectangleMousemoveDrawing
         * @param data 从服务器接收到的消息，包含绘图的操作数据
         */
        rectangleMousemoveDrawing: function (data) {
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
            if (this.originPoint === null) {
                return
            }
            if (this.isOutCanvas(data) === true) {
                return
            }
            this.circleMousemoveDrawing(data)
        },
        /**
         * 绘制圆形，在circleMousemove函数中调用
         *
         * @method circleMousemoveDrawing
         * @param data 从服务器接收到的信息，包含画图操作的数据
         */
        circleMousemoveDrawing: function (data) {
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
            if (this.originPoint === null) {
                return
            }
            if (this.isOutCanvas(data) === true) {
                return
            }
            this.ellipseMousemoveDrawing(data)
        },
        /**
         * 绘制椭圆，在ellipseMousemove函数中调用
         *
         * @method ellipseMousemoveDrawing
         * @param data 从服务器接收到的消息，包含画图操作的各种数据
         */
        ellipseMousemoveDrawing: function (data) {
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
        boardUndo: function (data) {
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
                this.clear(data)
            } else if (data.type === 'textField') {
                this.textBox(data)
            } else if (data.type === 'drawText') {
                this.font(data)
            } else if (data.type === 'undo') {
                this.boardUndo(data)
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
.white-board {
    height: 100%;
    display: flex;
    cursor: hand;
}

.drawing-board {
    height: 100%;
    width: 100%;
}
</style>
