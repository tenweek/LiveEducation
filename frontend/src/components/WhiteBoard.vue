<template>
    <div class="white-board">
        <div class="tools">
            <div class="undo-redo">
                <Button class="button-undo-redo" @click="undo"><Icon type="reply"></Icon></Button>
                <Button class="button-undo-redo" @click="redo"><Icon type="forward"></Icon></Button>
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
            <canvas ref="board" class="canvas" :width="WIDTH" :height="HEIGHT"></canvas>
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

    created () {
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
            WIDTH: 601,
            HEIGHT: 486,
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
            this.socket.emit('drawing', {
                type: 'clear',
            }, this.roomId + '.0')
            return
        },

        undo: function () {
            this.socket.emit('drawing', {
                type: 'undo',
            }, this.roomId + '.0')
        },

        redo: function () {
            this.socket.emit('drawing', {
                type: 'redo',
            }, this.roomId + '.0')
        },

        penCommand: function (action, { x, y, buttons}) {
            let color = this.colorBorder
            let size = this.size
            this.socket.emit('drawing', {
                type: 'pen',
                action: action,
                x: x,
                y: y,
                buttons: buttons,
                color: color,
                size: size,
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
                size: size,
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
                size: size,
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
                size: size,
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
                size: size,
            }, this.roomId + '.0')
        }
    },

    mounted () {
        if (this.operational) {
            ['mousemove', 'mousedown', 'mouseup'].map((eventName) => {
                this.$refs.board.addEventListener(eventName, ({ offsetX: x, offsetY: y, buttons }) => {
                    this[`${this.type}Command`](eventName, { x, y, buttons } )
                })
            })
        }
        this.context = this.$refs.board.getContext('2d')
        this.allImageData.push(this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT))
        let vueThis = this
        this.socket = io.connect('http://localhost:9000')
        this.socket.emit('join', this.roomId + '.0')
        this.socket.on('drawing', function(data) {
            let xData = data.x
            let yData = data.y
            let buttonsData = data.buttons
            switch (data.type) {
                case 'pen':
                vueThis.size = data.size
                vueThis.colorBorder = data.color
                if (data.action === 'mousedown') {
                    vueThis.penOriginPoint = [data.x, data.y]
                    vueThis.lastImageData = vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT)
                } else if (data.action === 'mousemove') {
                    if (vueThis.penOriginPoint === null) {
                        return
                    }
                    const context = vueThis.context
                    const [ ox, oy ] = vueThis.penOriginPoint
                    context.strokeStyle = vueThis.colorBorder
                    context.lineWidth = vueThis.size
                    context.beginPath()
                    context.moveTo(ox, oy)
                    context.lineTo(xData, yData)
                    context.stroke()
                    context.closePath()
                    vueThis.penOriginPoint = [xData, yData]
                } else if (data.action === 'mouseup') {
                    vueThis.penOriginPoint = null
                    vueThis.lastImageData = null
                    vueThis.allImageData.length = vueThis.pointer + 1
                    vueThis.allImageData.push(vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT))
                    vueThis.pointer = vueThis.allImageData.length - 1
                }
                break
                case 'eraser':
                vueThis.size = data.size
                switch (data.action) {
                    case 'mousedown':
                    vueThis.circleOriginPoint = [xData, yData]
                    vueThis.lastImageData = vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT)
                    break
                    case 'mousemove':
                    if (vueThis.circleOriginPoint === null) {
                        return
                    }
                    const context = vueThis.context
                    const [ ox, oy ] = vueThis.circleOriginPoint
                    context.clearRect(ox, oy, vueThis.size * 10, vueThis.size * 10)
                    vueThis.circleOriginPoint = [xData, yData]
                    break
                    case 'mouseup':
                    vueThis.circleOriginPoint = null
                    vueThis.lastImageData = null
                    vueThis.allImageData.length = vueThis.pointer + 1
                    vueThis.allImageData.push(vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT))
                    vueThis.pointer = vueThis.allImageData.length - 1
                    break
                }
                break
                case 'line':
                vueThis.colorBorder = data.color
                vueThis.size = data.size
                switch (data.action) {
                    case 'mousedown':
                    vueThis.lineOriginPoint = [xData, yData]
                    vueThis.lastImageData = vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT)
                    break
                    case 'mousemove':
                    if (vueThis.lineOriginPoint == null) {
                        return
                    }
                    const context = vueThis.context
                    context.putImageData(vueThis.lastImageData, 0, 0)
                    const [ ox, oy ] = vueThis.lineOriginPoint
                    context.strokeStyle = vueThis.colorBorder
                    context.lineWidth = vueThis.size
                    context.beginPath()
                    context.moveTo(ox, oy)
                    context.lineTo(xData, yData)
                    context.stroke()
                    context.closePath()
                    break
                    case 'mouseup':
                    vueThis.lineOriginPoint = null
                    vueThis.lastImageData = null
                    vueThis.allImageData.length = vueThis.pointer + 1
                    vueThis.allImageData.push(vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT))
                    vueThis.pointer = vueThis.allImageData.length - 1
                    break
                }
                break
                case 'rectangle':
                vueThis.colorBorder = data.colorBorder
                vueThis.colorFill = data.colorFill
                vueThis.fill = data.fill
                vueThis.size = data.size
                switch (data.action) {
                    case 'mousedown':
                    vueThis.circleOriginPoint = [xData, yData]
                    vueThis.lastImageData = vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT)
                    break
                    case 'mousemove':
                    if (vueThis.circleOriginPoint === null) {
                    return
                    }
                    const context = vueThis.context
                    context.putImageData(vueThis.lastImageData, 0, 0)
                    const [ ox, oy ] = vueThis.circleOriginPoint
                    const [ dx, dy ] = [ xData - ox, yData - oy ]
                    context.lineWidth = vueThis.size
                    context.beginPath()
                    context.rect(ox, oy, dx, dy)
                    if (vueThis.fill === true) {
                        context.fillStyle = vueThis.colorFill
                        context.fill()
                    }
                    if (vueThis.border === true) {
                        context.strokeStyle = vueThis.colorBorder
                        context.stroke()
                    }
                    context.closePath()
                    break
                    case 'mouseup':
                    vueThis.circleOriginPoint = null
                    vueThis.lastImageData = null
                    vueThis.allImageData.length = vueThis.pointer + 1
                    vueThis.allImageData.push(vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT))
                    vueThis.pointer = vueThis.allImageData.length - 1
                    break
                }
                break
                case 'circle':
                vueThis.colorBorder = data.colorBorder
                vueThis.colorFill = data.colorFill
                vueThis.fill = data.fill
                vueThis.size = data.size
                switch (data.action) {
                    case 'mousedown':
                    vueThis.circleOriginPoint = [xData, yData]
                    vueThis.lastImageData = vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT)
                    break
                    case 'mousemove':
                    if (vueThis.circleOriginPoint === null) {
                        return
                    }
                    const context = vueThis.context
                    context.putImageData(vueThis.lastImageData, 0, 0)
                    const [ ox, oy ] = vueThis.circleOriginPoint
                    const [ dx, dy ] = [ xData - ox, yData - oy ]
                    const radius = Math.sqrt(dx * dx, dy * dy)
                    context.lineWidth = vueThis.size
                    context.beginPath()
                    context.arc((ox + xData) / 2, (yData + oy) / 2, radius, 0, 2 * Math.PI)
                    if (vueThis.fill === true) {
                        context.fillStyle = vueThis.colorFill
                        context.fill()
                    }
                    if (vueThis.border === true) {
                        context.strokeStyle = vueThis.colorBorder
                        context.stroke()
                    }
                    context.closePath()
                    break
                    case 'mouseup':
                    vueThis.circleOriginPoint = null
                    vueThis.lastImageData = null
                    vueThis.allImageData.length = vueThis.pointer + 1
                    vueThis.allImageData.push(vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT))
                    vueThis.pointer = vueThis.allImageData.length - 1
                    break
                }
                break
                case 'ellipse':
                vueThis.colorBorder = data.colorBorder
                vueThis.colorFill = data.colorFill
                vueThis.fill = data.fill
                vueThis.size = data.size
                switch (data.action) {
                    case 'mousedown':
                    vueThis.circleOriginPoint = [xData, yData]
                    vueThis.lastImageData = vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT)
                    break
                    case 'mousemove':
                    if (vueThis.circleOriginPoint === null) {
                    return
                    }
                    const context = vueThis.context
                    context.putImageData(vueThis.lastImageData, 0, 0)
                    const [ ox, oy ] = vueThis.circleOriginPoint
                    const [ dx, dy ] = [ xData - ox, yData - oy ]
                    context.strokeStyle = vueThis.colorBorder
                    context.lineWidth = vueThis.size
                    if (vueThis.fill === true) {
                        context.fillStyle = vueThis.colorFill
                    }
                    context.beginPath()
                    context.ellipse((xData + ox) / 2, (yData + oy) / 2, dx / 2, dy / 2, 0, 0, 2 * Math.PI)
                    if (vueThis.fill === true) {
                        context.fillStyle = vueThis.colorFill
                        context.fill()
                    }
                    if (vueThis.border === true) {
                        context.strokeStyle = vueThis.colorBorder
                        context.stroke()
                    }
                    context.closePath()
                    break
                    case 'mouseup':
                    vueThis.circleOriginPoint = null
                    vueThis.lastImageData = null
                    vueThis.allImageData.length = vueThis.pointer + 1
                    vueThis.allImageData.push(vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT))
                    vueThis.pointer = vueThis.allImageData.length - 1
                    break
                }
                break
                case 'clear':
                vueThis.context.clearRect(0, 0, vueThis.WIDTH, vueThis.HEIGHT)
                vueThis.allImageData.push(vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT))
                vueThis.pointer += 1
                break
                case 'textField':
                if (data.action === 'mouseup') {
                    vueThis.textLeft = xData
                    vueThis.textTop =  yData
                }
                break
                case 'drawText':
                vueThis.textField = false
                vueThis.context.fillText(data.input, vueThis.textLeft, vueThis.textTop)
                vueThis.textInput = ''
                vueThis.allImageData.push(vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT))
                vueThis.pointer = vueThis.allImageData.length - 1
                break
                case 'undo':
                if (vueThis.pointer === 0) {
                    alert('没有可撤销的操作')
                    return
                }
                if (vueThis.pointer > 0) {
                    vueThis.pointer -= 1
                }
                vueThis.context.putImageData(vueThis.allImageData[vueThis.pointer], 0, 0)
                vueThis.allImageData.push(vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT))
                return
                case 'redo':
                if (vueThis.pointer === vueThis.allImageData.length - 1) {
                    alert('已没有可重做的操作')
                    return
                }
                if (vueThis.pointer < vueThis.allImageData.length) {
                    vueThis.pointer += 1
                }
                vueThis.context.putImageData(vueThis.allImageData[vueThis.pointer], 0, 0)
                vueThis.allImageData.push(vueThis.context.getImageData(0, 0, vueThis.WIDTH, vueThis.HEIGHT))
                }
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
