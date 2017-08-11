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
            <Button type="text" :class="{ active: type === 'eraser' }" @click="type = 'eraser'">橡皮擦</Button>
            <Button type="text" :class="{ active: type === 'pen' }" @click="type = 'pen'">画笔</Button>
            <Button type="text" :class="{ active: type === 'text' }" @click="type = 'text'">文字</Button>
            <Button type="text" :class="{ active: type === 'line' }" @click="type = 'line'">直线</Button>
            <Button type="text" :class="{ active: type === 'rectangle' }" @click="type = 'rectangle'">矩形</Button>
            <Button type="text" :class="{ active: type === 'circle' }" @click="type = 'circle'">圆形</Button>
            <Button type="text" :class="{ active: type === 'ellipse' }" @click="type = 'ellipse'">椭圆</Button>
            <Button type="text" :class="{ active: border === true }" @click="border = !border">边框</Button>
            <Button type="text" :class="{ active: fill === true }" @click="fill = !fill">填充</Button>
            <el-color-picker class="color-selected" v-model="colorBorder" show-alpha></el-color-picker>
            <el-color-picker class="color-selected" v-model="colorFill" show-alpha></el-color-picker>
            <div class="size">
                <label class="size-label">粗细</label>
                <div class="size-buttons">
                    <Button type="text" :class="{ active: size === 5 }" id="size-button" @click="size = 5">大</Button>
                    <Button type="text" :class="{ active: size === 3 }" id="size-button" @click="size = 3">中</Button>
                    <Button type="text" :class="{ active: size === 1 }" id="size-button" @click="size = 1">小</Button>
                </div>
            </div>
    
        </div>
    
        <div class="drawing-board">
            <input id="text-field" @keyup.enter="drawText" v-show="this.textField === true" v-model="textInput" placeholder="请输入..." autofocus="true" style="width: 300px"></input>
            <canvas ref="board" class="canvas" :width="width" :height="height"></canvas>
        </div>
    
    </div>
</template>

<script src="/socket.io/socket.io.js"></script>

<script>
import * as io from 'socket.io-client'
export default {
    name: 'white-board',
    props: {
        operational: {
            type: Boolean,
            default: true
        }
    },

    created: function () {
        this.roomId = this.$route.params.id
    },

    data: function () {
        return {
            type: 'pen',
            context: null,
            penOriginPoint: null,
            lineOriginPoint: null,
            circleOriginPoint: null,
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
        drawText: function () {
            let input = this.textInput
            this.socket.emit('drawing', {
                type: 'drawText',
                input: input
            }, this.roomId + '.0')
            return
        },
        clear: function () {
            this.socket.emit('drawing', { type: 'clear' }, this.roomId + '.0')
            return
        },
        undo: function () {
            this.socket.emit('drawing', { type: 'undo' }, this.roomId + '.0')
        },
        redo: function () {
            this.socket.emit('drawing', { type: 'redo' }, this.roomId + '.0')
        },
        penCommand: function (action, { x, y, buttons }) {
            let color = this.colorBorder
            let size = this.size
            this.socket.emit('drawing', {
                type: 'pen',
                action: action,
                x: x,
                y: y,
                buttons: buttons,
                color: color,
                size: size
            }, this.roomId + '.0')
        },
        textCommand: function (action, { x, y, buttons }) {
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
            return
        },
        eraserCommand: function (action, { x, y, buttons }) {
            let size = this.size
            this.socket.emit('drawing', {
                type: 'eraser',
                action: action,
                x: x,
                y: y,
                buttons: buttons,
                size: size
            }, this.roomId + '.0')
        },
        lineCommand: function (action, { x, y, buttons }) {
            let color = this.colorBorder
            let size = this.size
            this.socket.emit('drawing', {
                type: 'line',
                action: action,
                x: x,
                y: y,
                buttons: buttons,
                color: color,
                size: size
            }, this.roomId + '.0')
        },
        rectangleCommand: function (action, { x, y, buttons }) {
            let colorBorder = this.colorBorder
            let colorFill = this.colorFill
            let fill = this.fill
            let size = this.size
            this.socket.emit('drawing', {
                type: 'rectangle',
                action: action,
                x: x,
                y: y,
                buttons: buttons,
                colorBorder: colorBorder,
                colorFill: colorFill,
                fill: fill,
                size: size
            }, this.roomId + '.0')
        },
        circleCommand: function (action, { x, y, buttons }) {
            let colorBorder = this.colorBorder
            let colorFill = this.colorFill
            let fill = this.fill
            let size = this.size
            this.socket.emit('drawing', {
                type: 'circle',
                action: action,
                x: x,
                y: y,
                buttons: buttons,
                colorBorder: colorBorder,
                colorFill: colorFill,
                fill: fill,
                size: size
            }, this.roomId + '.0')
        },
        ellipseCommand: function (action, { x, y, buttons }) {
            let colorBorder = this.colorBorder
            let colorFill = this.colorFill
            let fill = this.fill
            let size = this.size
            this.socket.emit('drawing', {
                type: 'ellipse',
                action: action,
                x: x,
                y: y,
                buttons: buttons,
                colorBorder: colorBorder,
                colorFill: colorFill,
                fill: fill,
                size: size
            }, this.roomId + '.0')
        },
        pen: function (data, xData, yData) {
            this.size = data.size
            this.colorBorder = data.color
            if (data.action === 'mousedown') {
                this.penOriginPoint = [data.x, data.y]
                this.lastImageData = this.context.getImageData(0, 0, this.width, this.height)
            } else if (data.action === 'mousemove') {
                if (this.penOriginPoint === null) {
                    return
                }
                const context = this.context
                const [ox, oy] = this.penOriginPoint
                context.strokeStyle = this.colorBorder
                context.linewidth = this.size
                context.beginPath()
                context.moveTo(ox, oy)
                context.lineTo(xData, yData)
                context.stroke()
                context.closePath()
                this.penOriginPoint = [xData, yData]
            } else if (data.action === 'mouseup') {
                this.penOriginPoint = null
                this.lastImageData = null
                this.allImageData.length = this.pointer + 1
                this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
                this.pointer = this.allImageData.length - 1
            }
        },
        eraser: function (data, xData, yData) {
            this.size = data.size
            switch (data.action) {
                case 'mousedown':
                    this.circleOriginPoint = [xData, yData]
                    this.lastImageData = this.context.getImageData(0, 0, this.width, this.height)
                    break
                case 'mousemove':
                    if (this.circleOriginPoint === null) {
                        return
                    }
                    const context = this.context
                    const [ox, oy] = this.circleOriginPoint
                    context.clearRect(ox, oy, this.size * 10, this.size * 10)
                    this.circleOriginPoint = [xData, yData]
                    break
                case 'mouseup':
                    this.circleOriginPoint = null
                    this.lastImageData = null
                    this.allImageData.length = this.pointer + 1
                    this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
                    this.pointer = this.allImageData.length - 1
                    break
            }
        },
        line: function (data, xData, yData) {
            this.colorBorder = data.color
            this.size = data.size
            switch (data.action) {
                case 'mousedown':
                    this.lineOriginPoint = [xData, yData]
                    this.lastImageData = this.context.getImageData(0, 0, this.width, this.height)
                    break
                case 'mousemove':
                    if (this.lineOriginPoint == null) {
                        return
                    }
                    const context = this.context
                    context.putImageData(this.lastImageData, 0, 0)
                    const [ox, oy] = this.lineOriginPoint
                    context.strokeStyle = this.colorBorder
                    context.linewidth = this.size
                    context.beginPath()
                    context.moveTo(ox, oy)
                    context.lineTo(xData, yData)
                    context.stroke()
                    context.closePath()
                    break
                case 'mouseup':
                    this.lineOriginPoint = null
                    this.lastImageData = null
                    this.allImageData.length = this.pointer + 1
                    this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
                    this.pointer = this.allImageData.length - 1
                    break
            }
        },
        rectangle: function (data, xData, yData) {
            this.colorBorder = data.colorBorder
            this.colorFill = data.colorFill
            this.fill = data.fill
            this.size = data.size
            switch (data.action) {
                case 'mousedown':
                    this.circleOriginPoint = [xData, yData]
                    this.lastImageData = this.context.getImageData(0, 0, this.width, this.height)
                    break
                case 'mousemove':
                    if (this.circleOriginPoint === null) {
                        return
                    }
                    const context = this.context
                    context.putImageData(this.lastImageData, 0, 0)
                    const [ox, oy] = this.circleOriginPoint
                    const [dx, dy] = [xData - ox, yData - oy]
                    context.linewidth = this.size
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
                    this.circleOriginPoint = null
                    this.lastImageData = null
                    this.allImageData.length = this.pointer + 1
                    this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
                    this.pointer = this.allImageData.length - 1
                    break
            }
        },
        circle: function (data, xData, yData) {
            this.colorBorder = data.colorBorder
            this.colorFill = data.colorFill
            this.fill = data.fill
            this.size = data.size
            switch (data.action) {
                case 'mousedown':
                    this.circleOriginPoint = [xData, yData]
                    this.lastImageData = this.context.getImageData(0, 0, this.width, this.height)
                    break
                case 'mousemove':
                    if (this.circleOriginPoint === null) {
                        return
                    }
                    const context = this.context
                    context.putImageData(this.lastImageData, 0, 0)
                    const [ox, oy] = this.circleOriginPoint
                    const [dx, dy] = [xData - ox, yData - oy]
                    const radius = Math.sqrt(dx * dx, dy * dy)
                    context.linewidth = this.size
                    context.beginPath()
                    context.arc((ox + xData) / 2, (yData + oy) / 2, radius, 0, 2 * Math.PI)
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
                    this.circleOriginPoint = null
                    this.lastImageData = null
                    this.allImageData.length = this.pointer + 1
                    this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
                    this.pointer = this.allImageData.length - 1
                    break
            }
        },
        ellipse: function (data, xData, yData) {
            this.colorBorder = data.colorBorder
            this.colorFill = data.colorFill
            this.fill = data.fill
            this.size = data.size
            switch (data.action) {
                case 'mousedown':
                    this.circleOriginPoint = [xData, yData]
                    this.lastImageData = this.context.getImageData(0, 0, this.width, this.height)
                    break
                case 'mousemove':
                    if (this.circleOriginPoint === null) {
                        return
                    }
                    const context = this.context
                    context.putImageData(this.lastImageData, 0, 0)
                    const [ox, oy] = this.circleOriginPoint
                    const [dx, dy] = [xData - ox, yData - oy]
                    context.strokeStyle = this.colorBorder
                    context.linewidth = this.size
                    if (this.fill === true) {
                        context.fillStyle = this.colorFill
                    }
                    context.beginPath()
                    context.ellipse((xData + ox) / 2, (yData + oy) / 2, dx / 2, dy / 2, 0, 0, 2 * Math.PI)
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
                    this.circleOriginPoint = null
                    this.lastImageData = null
                    this.allImageData.length = this.pointer + 1
                    this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
                    this.pointer = this.allImageData.length - 1
                    break
            }
        },
        boardClear: function (data, xData, yData) {
            this.context.clearRect(0, 0, this.width, this.height)
            this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
            this.pointer += 1
        },
        textBox: function (data, xData, yData) {
            if (data.action === 'mouseup') {
                this.textLeft = xData
                this.textTop = yData
            }
        },
        font: function (data, xData, yData) {
            this.textField = false
            this.context.fillText(data.input, this.textLeft, this.textTop)
            this.textInput = ''
            this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
            this.pointer = this.allImageData.length - 1
        },
        boardUndo: function (data, xData, yData) {
            if (this.pointer === 0) {
                alert('没有可撤销的操作')
                return
            }
            if (this.pointer > 0) {
                this.pointer -= 1
            }
            this.context.putImageData(this.allImageData[this.pointer], 0, 0)
            this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
        },
        boardRedo: function (data, xData, yData) {
            if (this.pointer === this.allImageData.length - 1) {
                alert('已没有可重做的操作')
                return
            }
            if (this.pointer < this.allImageData.length) {
                this.pointer += 1
            }
            this.context.putImageData(this.allImageData[this.pointer], 0, 0)
            this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
        },
        whiteBoardDoing: function (data, xData, yData) {
            switch (data.type) {
                case 'pen':
                    this.pen(data, xData, yData)
                    break
                case 'eraser':
                    this.eraser(data, xData, yData)
                    break
                case 'line':
                    this.line(data, xData, yData)
                    break
                case 'rectangle':
                    this.rectangle(data, xData, yData)
                    break
                case 'circle':
                    this.circle(data, xData, yData)
                    break
                case 'ellipse':
                    this.ellipse(data, xData, yData)
                    break
                case 'clear':
                    this.boardClear(data, xData, yData)
                    break
                case 'textField':
                    this.textBox(data, xData, yData)
                    break
                case 'drawText':
                    this.font(data, xData, yData)
                    break
                case 'undo':
                    this.boardUndo(data, xData, yData)
                    break
                case 'redo':
                    this.boardRedo(data, xData, yData)
                    break
            }
        }
    },
    mounted: function () {
        if (this.operational) {
            ['mousemove', 'mousedown', 'mouseup'].map((eventName) => {
                this.$refs.board.addEventListener(eventName, ({ offsetX: x, offsetY: y, buttons }) => {
                    this[`${this.type}Command`](eventName, { x, y, buttons })
                })
            })
        }
        this.context = this.$refs.board.getContext('2d')
        this.allImageData.push(this.context.getImageData(0, 0, this.width, this.height))
        let self = this
        this.socket = io.connect('http://localhost:9000')
        this.socket.emit('joinForWhiteBoard', this.roomId + '.0')
        this.socket.on('drawing', function (data) {
            let xData = data.x
            let yData = data.y
            self.whiteBoardDoing(data, xData, yData)
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
}

.canvas {
    background: white;
}
</style>
