<template>
    <div class="white-board">
        <div class="tools">
            <div class="undo-redo">
                <Button class="button-undo-redo" @click="undo">
                    <Icon type="reply"></Icon>
                </Button>
                <Button class="button-undo-redo" @click="redo">
                    <Icon type="forward"></Icon>
                </Button>
            </div>
            <Button class="clear" @click="clear">清空</Button>
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
                <Dropdown-menu slot="list">
                    <Dropdown-item name='small'>小</Dropdown-item></Dropdown-item>
                    <Dropdown-item name='middle'>中</Dropdown-item>
                    <Dropdown-item name='large'>大</Dropdown-item>
                </Dropdown-menu>
            </Dropdown>
            <Button type="text" :class="{ active: border === true }" @click="clickBorder">边框</Button>
            <Button type="text" :class="{ active: fill === true }" @click="clickFill">填充</Button>
            <el-color-picker class="color-selected" v-model="colorBorder" show-alpha></el-color-picker>
            <el-color-picker class="color-selected" v-model="colorFill" show-alpha></el-color-picker>
        </div>
        <div class="drawing-board">
            <input id="text-field" @keyup.enter="drawText" v-show="this.textField === true" v-model="textInput" placeholder="请输入..." autofocus="true" style="width: 300px"></input>
            <canvas ref="board" :class="this.type === 'eraser' ? 'canvas-eraser' : 'canvas-drawing'" :width="width" :height="height"></canvas>
        </div>
    </div>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
import * as io from 'socket.io-client'
import myMsg from './../warning.js'
export default {
    name: 'white-board',
    props: ['roomId', 'teacherName', 'username'],
    data: function () {
        return {
            type: 'pen',
            context: null,
            originPoint: null,
            lastImageData: null,
            width: 601,
            height: 486,
            colorBorder: 'rgba(0, 0, 0, 1)',
            colorFill: 'rgba(255, 255, 255, 1)',
            fill: false,
            border: true,
            size: 1,
            textField: false,
            textInput: '',
            textLeft: 10,
            textTop: 50,
            allImageData: [],
            currentImageData: null,
            pointer: 0,
            socket: '',
            roomId: ''
        }
    },
    methods: {
        changeSize: function (name) {
            if (name === 'large') {
                if (this.teacherName !== this.username) {
                    return
                }
                this.socket.emit('click', { type: 'sizeLarge' }, this.roomId + '.0')
                console.log('点击了size-large, emit之后')
                console.log(this.size)
            } else if (name === 'middle') {
                if (this.teacherName !== this.username) {
                    return
                }
                this.socket.emit('click', { type: 'sizeMiddle' }, this.roomId + '.0')
            } else {
                if (this.teacherName !== this.username) {
                    return
                }
                this.socket.emit('click', { type: 'sizeSmall' }, this.roomId + '.0')
            }
            console.log(this.size)
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
            this.socket.emit('drawing', {
                type: 'drawText',
                input: input
            }, this.roomId + '.0')
        },
        clear: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('drawing', { type: 'clear' }, this.roomId + '.0')
        },
        undo: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('drawing', { type: 'undo' }, this.roomId + '.0')
        },
        redo: function () {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('drawing', { type: 'redo' }, this.roomId + '.0')
        },
        penCommand: function (action, { x, y, buttons }) {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('drawing', {
                type: 'pen',
                action: action,
                x: x,
                y: y,
                buttons: buttons,
                color: this.colorBorder,
                size: this.size
            }, this.roomId + '.0')
        },
        textCommand: function (action, { x, y, buttons }) {
            if (this.teacherName !== this.username) {
                return
            }
            if (action === 'mouseup') {
                this.textField = true
                this.socket.emit('drawing', {
                    type: 'textField',
                    x: x,
                    y: y,
                    action: action,
                    buttons: buttons
                }, this.roomId + '.0')
            }
        },
        eraserCommand: function (action, { x, y, buttons }) {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('drawing', {
                type: 'eraser',
                action: action,
                x: x,
                y: y,
                buttons: buttons,
                size: this.size
            }, this.roomId + '.0')
        },
        lineCommand: function (action, { x, y, buttons }) {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('drawing', {
                type: 'line',
                action: action,
                x: x,
                y: y,
                buttons: buttons,
                color: this.colorBorder,
                size: this.size
            }, this.roomId + '.0')
        },
        rectangleCommand: function (action, { x, y, buttons }) {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('drawing', {
                type: 'rectangle',
                action: action,
                x: x,
                y: y,
                buttons: buttons,
                colorBorder: this.colorBorder,
                colorFill: this.colorFill,
                fill: this.fill,
                size: this.size
            }, this.roomId + '.0')
        },
        circleCommand: function (action, { x, y, buttons }) {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('drawing', {
                type: 'circle',
                action: action,
                x: x,
                y: y,
                buttons: buttons,
                colorBorder: this.colorBorder,
                colorFill: this.colorFill,
                fill: this.fill,
                size: this.size
            }, this.roomId + '.0')
        },
        ellipseCommand: function (action, { x, y, buttons }) {
            if (this.teacherName !== this.username) {
                return
            }
            this.socket.emit('drawing', {
                type: 'ellipse',
                action: action,
                x: x,
                y: y,
                buttons: buttons,
                colorBorder: this.colorBorder,
                colorFill: this.colorFill,
                fill: this.fill,
                size: this.size
            }, this.roomId + '.0')
        },
        pen: function (data) {
            this.size = data.size
            this.colorBorder = data.color
            if (data.action === 'mousedown') {
                this.originPoint = [data.x, data.y]
                this.lastImageData = this.context.getImageData(0, 0, this.width, this.height)
            } else if (data.action === 'mousemove') {
                if (this.originPoint === null) {
                    return
                }
                const context = this.context
                const [ox, oy] = this.originPoint
                context.strokeStyle = this.colorBorder
                context.lineWidth = this.size
                context.beginPath()
                context.moveTo(ox, oy)
                context.lineTo(data.x, data.y)
                context.stroke()
                context.closePath()
                this.originPoint = [data.x, data.y]
            } else if (data.action === 'mouseup') {
                this.originPoint = null
                this.lastImageData = null
                this.allImageData.length = this.pointer + 1
                this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
                this.pointer = this.allImageData.length - 1
            }
        },
        eraser: function (data) {
            this.size = data.size
            switch (data.action) {
                case 'mousedown':
                    this.originPoint = [data.x, data.y]
                    this.lastImageData = this.context.getImageData(0, 0, this.width, this.height)
                    break
                case 'mousemove':
                    if (this.originPoint === null) {
                        return
                    }
                    const context = this.context
                    const [ox, oy] = this.originPoint
                    context.clearRect(ox, oy, this.size * 10, this.size * 10)
                    this.originPoint = [data.x, data.y]
                    break
                case 'mouseup':
                    this.originPoint = null
                    this.lastImageData = null
                    this.allImageData.length = this.pointer + 1
                    this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
                    this.pointer = this.allImageData.length - 1
                    break
            }
        },
        line: function (data) {
            this.colorBorder = data.color
            this.size = data.size
            switch (data.action) {
                case 'mousedown':
                    this.originPoint = [data.x, data.y]
                    this.lastImageData = this.context.getImageData(0, 0, this.width, this.height)
                    break
                case 'mousemove':
                    if (this.originPoint == null) {
                        return
                    }
                    const context = this.context
                    context.putImageData(this.lastImageData, 0, 0)
                    const [ox, oy] = this.originPoint
                    context.strokeStyle = this.colorBorder
                    context.lineWidth = this.size
                    context.beginPath()
                    context.moveTo(ox, oy)
                    context.lineTo(data.x, data.y)
                    context.stroke()
                    context.closePath()
                    break
                case 'mouseup':
                    this.originPoint = null
                    this.lastImageData = null
                    this.allImageData.length = this.pointer + 1
                    this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
                    this.pointer = this.allImageData.length - 1
                    break
            }
        },
        rectangle: function (data) {
            this.colorBorder = data.colorBorder
            this.colorFill = data.colorFill
            this.fill = data.fill
            this.size = data.size
            switch (data.action) {
                case 'mousedown':
                    this.originPoint = [data.x, data.y]
                    this.lastImageData = this.context.getImageData(0, 0, this.width, this.height)
                    break
                case 'mousemove':
                    if (this.originPoint === null) {
                        return
                    }
                    const context = this.context
                    context.putImageData(this.lastImageData, 0, 0)
                    const [ox, oy] = this.originPoint
                    const [dx, dy] = [data.x - ox, data.y - oy]
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
                    this.allImageData.length = this.pointer + 1
                    this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
                    this.pointer = this.allImageData.length - 1
                    break
            }
        },
        circle: function (data) {
            this.colorBorder = data.colorBorder
            this.colorFill = data.colorFill
            this.fill = data.fill
            this.size = data.size
            switch (data.action) {
                case 'mousedown':
                    this.originPoint = [data.x, data.y]
                    this.lastImageData = this.context.getImageData(0, 0, this.width, this.height)
                    break
                case 'mousemove':
                    if (this.originPoint === null) {
                        return
                    }
                    const context = this.context
                    context.putImageData(this.lastImageData, 0, 0)
                    const [ox, oy] = this.originPoint
                    const [dx, dy] = [data.x - ox, data.y - oy]
                    const radius = Math.sqrt(dx * dx, dy * dy)
                    context.lineWidth = this.size
                    context.beginPath()
                    context.arc((ox + data.x) / 2, (data.y + oy) / 2, radius, 0, 2 * Math.PI)
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
                    this.allImageData.length = this.pointer + 1
                    this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
                    this.pointer = this.allImageData.length - 1
                    break
            }
        },
        ellipse: function (data) {
            this.colorBorder = data.colorBorder
            this.colorFill = data.colorFill
            this.fill = data.fill
            this.size = data.size
            switch (data.action) {
                case 'mousedown':
                    this.originPoint = [data.x, data.y]
                    this.lastImageData = this.context.getImageData(0, 0, this.width, this.height)
                    break
                case 'mousemove':
                    if (this.originPoint === null) {
                        return
                    }
                    const context = this.context
                    context.putImageData(this.lastImageData, 0, 0)
                    const [ox, oy] = this.originPoint
                    const [dx, dy] = [Math.abs(data.x - ox), Math.abs(data.y - oy)]
                    context.strokeStyle = this.colorBorder
                    context.lineWidth = this.size
                    if (this.fill === true) {
                        context.fillStyle = this.colorFill
                    }
                    context.beginPath()
                    context.ellipse((data.x + ox) / 2, (data.y + oy) / 2, dx / 2, dy / 2, 0, 0, 2 * Math.PI)
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
                    this.allImageData.length = this.pointer + 1
                    this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
                    this.pointer = this.allImageData.length - 1
                    break
            }
        },
        boardClear: function (data) {
            this.context.clearRect(0, 0, this.width, this.height)
            this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
            this.pointer += 1
        },
        textBox: function (data) {
            if (data.action === 'mouseup') {
                this.textLeft = data.x
                this.textTop = data.y
            }
        },
        font: function (data) {
            this.textField = false
            this.context.fillText(data.input, this.textLeft, this.textTop)
            this.textInput = ''
            this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
            this.pointer = this.allImageData.length - 1
        },
        boardUndo: function (data) {
            if (this.pointer === 0) {
                this.$Message.alert(myMsg.whiteBoard['undoNotExist'])
                return
            }
            if (this.pointer > 0) {
                this.pointer -= 1
            }
            this.context.putImageData(this.allImageData[this.pointer], 0, 0)
            this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
        },
        boardRedo: function (data) {
            if (this.pointer === this.allImageData.length - 1) {
                this.$Message.alert(myMsg.whiteBoard['redoNotExist'])
                return
            }
            if (this.pointer < this.allImageData.length) {
                this.pointer += 1
            }
            this.context.putImageData(this.allImageData[this.pointer], 0, 0)
            this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
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
                case 'redo':
                    this.boardRedo(data)
                    break
            }
        },
        buttonDoing: function (data) {
            switch(data.type) {
                case 'eraser':
                    console.log('row 523')
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
        }
    },
    mounted: function () {
        ['mousemove', 'mousedown', 'mouseup'].map((eventName) => {
            this.$refs.board.addEventListener(eventName, ({ offsetX: x, offsetY: y, buttons }) => {
                this[`${this.type}Command`](eventName, { x, y, buttons })
            })
        })
        this.context = this.$refs.board.getContext('2d')
        this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
        let self = this
        this.socket = io.connect('http://localhost:9000')
        this.socket.emit('joinForWhiteBoard', this.roomId + '.0')
        this.socket.on('drawing', function (data) {
            self.whiteBoardDoing(data)
        })
        this.socket.on('click', function (data) {
            self.buttonDoing(data)
        })
    }
}
</script>

<style scoped>
#text-field {
    position: relative;
}

.undo-redo {
    display: flex;
}

.button-undo-redo {
    width: 37px;
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

.size {
    display: flex;
}

.size-label {
    width: 25px;
    height: 54px;
    font-size: 13px;
    padding-left: 5px;
    padding-top: 10px;
    border: 1px solid #aaa;
    margin-top: 1px;
}

.size-buttons {
    width: 49px;
}

#size-button {
    width: 49px;
    height: 17px;
    font-size: 8px;
    padding-top: 1px;
}

.drawing-board {
    height: 100%;
    width: 100%;
    background: blue;
}

.canvas-eraser {
    background: #D4EFDF;
}

.canvas-eraser:hover {
    background: #F0B27A;
    cursor: move;
}

.canvas-drawing {
    background: #D4EFDF;
}

.canvas-drawing:hover {
    background: #F9E79F;
    cursor: crosshair;
}
</style>