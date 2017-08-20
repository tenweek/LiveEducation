<template>
    <div class="white-board">
        <div class="drawing-board">
            <canvas ref="board" id="canvas" :width="teachingToolsWidth" :height="teachingToolsHeight"></canvas>
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
            roomId: ''
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
        initData: function () {
            this.context = this.$refs.board.getContext('2d')
            this.canvas = document.getElementById('canvas')
            this.canvas.style.cursor = 'default'
            this.allDataUrl.push(this.canvas.toDataURL())
            this.socket = io.connect('http://localhost:9000')
            this.socket.emit('joinTest', 888)
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
        pen: function (data) {
            this.colorBorder = data.color
            if (data.action === 'mousedown') {
                this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
                this.lastImageData = this.context.getImageData(0, 0, this.teachingToolsWidth, this.teachingToolsHeight)
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
                context.lineTo(data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight)
                context.stroke()
                context.closePath()
                this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
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
                    this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
                    this.lastImageData = this.context.getImageData(0, 0, this.teachingToolsWidth, this.teachingToolsHeight)
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
                    this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
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
                    this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
                    this.lastImageData = this.context.getImageData(0, 0, this.teachingToolsWidth, this.teachingToolsHeight)
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
                    context.lineTo(data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight)
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
                    this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
                    this.lastImageData = this.context.getImageData(0, 0, this.teachingToolsWidth, this.teachingToolsHeight)
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
                    this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
                    this.lastImageData = this.context.getImageData(0, 0, this.teachingToolsWidth, this.teachingToolsHeight)
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
                    this.originPoint = [data.x * this.teachingToolsWidth, data.y * this.teachingToolsHeight]
                    this.lastImageData = this.context.getImageData(0, 0, this.teachingToolsWidth, this.teachingToolsHeight)
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
