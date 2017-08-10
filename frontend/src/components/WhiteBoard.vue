<template>
    <div class="white-board">
        <div class="tools">
            <div class="undo-redo">
                <Button class="button-undo-redo" @click="undo"><Icon type="reply"></Icon></Button>
                <Button class="button-undo-redo" @click="redo"><Icon type="forward"></Icon></Button>
            </div>
            <Button class="clear" @click="clear">清空</Button>
            <Button type="text" :class="{ active: type === 'eraser' }" @click="type = 'eraser'">橡皮擦</Button>
            <Button type="text" :class="{ active: type === 'pen' }" @click="type = 'pen'"><Icon type="edit"></Icon>&nbsp;&nbsp;铅笔</Button>
            <Button type="text" :class="{ active: type === 'text' }" @click="type = 'text'">文字</Button>
            <Button type="text" :class="{ active: type === 'line' }" @click="type = 'line'">直线</Button>
            <Button type="text" :class="{ active: type === 'rectangle' }" @click="type = 'rectangle'">矩形</Button>
            <Button type="text" :class="{ active: type === 'circle' }" @click="type = 'circle'">圆形</Button>
            <Button type="text" :class="{ active: type === 'ellipse' }" @click="type = 'ellipse'">椭圆</Button>
            <Button type="text" :class="{ active: border === true }" @click="border = !border">边框</Button>
            <Button type="text" :class="{ active: fill === true }" @click="fill = !fill">填充</Button>
            <el-color-picker class="color-selected" v-model="color1" show-alpha></el-color-picker>
            <el-color-picker class="color-selected" v-model="color2" show-alpha></el-color-picker>
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
    data () {
        return {
            types: ['pen', 'line', 'circle', 'rectangle', 'eraser', 'ellipse', 'eraser', 'text'],
            type: 'pen',
            context: null,
            penOriginPoint: null,
            lineOriginPoint: null,
            circleOriginPoint: null,
            lastImageData: null,
            WIDTH: 601,
            HEIGHT: 486,
            color1: 'rgba(0, 0, 0, 1)',
            color2: 'rgba(255, 255, 255, 1)',
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
            socket: ''
        }
    },
    methods: {
        sendmes () {
            this.socket.emit('drawing','123456')
        },

        drawText () {
            console.log(window.innerHeight)
            this.textField = false
            this.context.fillText(this.textInput, this.textLeft, this.textTop)
            this.textInput = ''
            this.allImageData.push(this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT))
            //this.pointer += 1
            this.pointer = this.allImageData.length - 1
        },

        clear () {
            this.context.clearRect(0, 0, this.WIDTH, this.HEIGHT)
            this.allImageData.push(this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT))
            this.pointer += 1
            this.socket.emit('drawing', {
                //imageData: this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT)
                type0: 'clear',
            })
            return
        },

        undo () {
            if (this.pointer === 0) {
                alert('没有可撤销的操作')
                return
            }
            if (this.pointer > 0) {
                this.pointer -= 1
            }
            this.context.putImageData(this.allImageData[this.pointer], 0, 0)
            this.allImageData.push(this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT))
            //this.pointer += 1
            //this.pointer = this.allImageData.length - 1
        },

        redo () {
            if (this.pointer === this.allImageData.length - 1) {
                alert('已没有可重做的操作')
                return
            }
            if (this.pointer < this.allImageData.length) {
                this.pointer += 1
            }
            this.context.putImageData(this.allImageData[this.pointer], 0, 0)
            this.allImageData.push(this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT))
            //this.pointer += 1
            //this.pointer = this.allImageData.length - 1
        },

        commandpen (action, { x, y, buttons}) {
            switch (action) {
                case 'mousedown':
                this.penOriginPoint = [x, y]
                this.lastImageData = this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT)
                break
                case 'mousemove':
                if (this.penOriginPoint == null) {
                    return
                }
                const context = this.context
                const [ ox, oy ] = this.penOriginPoint
                context.strokeStyle = this.color1
                context.lineWidth = this.size
                context.beginPath()
                context.moveTo(ox, oy)
                context.lineTo(x, y)
                context.stroke()
                context.closePath()
                this.penOriginPoint = [x, y]
                break
                case 'mouseup':
                this.penOriginPoint = null
                this.lastImageData = null
                this.allImageData.push(this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT))
                //this.pointer += 1
                this.pointer = this.allImageData.length - 1
                break
            }
            this.socket.emit('drawing', {
                //imageData: this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT)
                type0: 'pen',
                action0: action,
                x0: x,
                y0: y,
                buttons0: buttons
            })
        },

        commandtext (action, { x, y, buttons }) {
            if (action === 'mouseup') {
                this.textField = true
                this.textLeft = x
                this.textTop =  y
            }
        },

        commanderaser (action, { x, y, buttons }) {
            switch (action) {
                case 'mousedown':
                this.circleOriginPoint = [x, y]
                this.lastImageData = this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT)
                break
                case 'mousemove':
                if (this.circleOriginPoint === null) {
                    return
                }
                const context = this.context
                const [ ox, oy ] = this.circleOriginPoint
                context.clearRect(ox, oy, this.size * 10, this.size * 10)
                this.circleOriginPoint = [x, y]
                break
                case 'mouseup':
                this.circleOriginPoint = null
                this.lastImageData = null
                this.allImageData.push(this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT))
                //this.pointer += 1
                this.pointer = this.allImageData.length - 1
                break
            }
            this.socket.emit('drawing', {
                //imageData: this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT)
                type0: 'eraser',
                action0: action,
                x0: x,
                y0: y,
                buttons0: buttons
            })
        },

        commandline (action, { x, y, buttons }) {
            switch (action) {
                case 'mousedown':
                this.lineOriginPoint = [x, y]
                this.lastImageData = this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT)
                break
                case 'mousemove':
                if (this.lineOriginPoint == null) {
                    return
                }
                const context = this.context
                context.putImageData(this.lastImageData, 0, 0)
                const [ ox, oy ] = this.lineOriginPoint
                context.strokeStyle = this.color1
                context.lineWidth = this.size
                context.beginPath()
                context.moveTo(ox, oy)
                context.lineTo(x, y)
                context.stroke()
                context.closePath()
                break
                case 'mouseup':
                this.lineOriginPoint = null
                this.lastImageData = null
                this.allImageData.push(this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT))
                //this.pointer += 1
                this.pointer = this.allImageData.length - 1
                break
            }
            this.socket.emit('drawing', {
                //imageData: this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT)
                type0: 'line',
                action0: action,
                x0: x,
                y0: y,
                buttons0: buttons
            })
        },

        commandrectangle (action, { x, y, buttons }) {
            switch (action) {
                case 'mousedown':
                this.circleOriginPoint = [x, y]
                this.lastImageData = this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT)
                break
                case 'mousemove':
                if (this.circleOriginPoint === null) {
                return
                }
                const context = this.context
                context.putImageData(this.lastImageData, 0, 0)
                const [ ox, oy ] = this.circleOriginPoint
                const [ dx, dy ] = [ x - ox, y - oy ]
                context.lineWidth = this.size
                context.beginPath()
                context.rect(ox, oy, dx, dy)
                if (this.fill === true) {
                    context.fillStyle = this.color2
                    context.fill()
                }
                if (this.border === true) {
                    context.strokeStyle = this.color1
                    context.stroke()
                }
                context.closePath()
                break
                case 'mouseup':
                this.circleOriginPoint = null
                this.lastImageData = null
                this.allImageData.push(this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT))
                //this.pointer += 1
                this.pointer = this.allImageData.length - 1
                break
            }
            this.socket.emit('drawing', {
                //imageData: this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT)
                type0: 'rectangle',
                action0: action,
                x0: x,
                y0: y,
                buttons0: buttons
            })
        },

        commandcircle (action, { x, y, buttons }) {
            switch (action) {
                case 'mousedown':
                this.circleOriginPoint = [x, y]
                this.lastImageData = this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT)
                break
                case 'mousemove':
                if (this.circleOriginPoint === null) {
                    return
                }
                const context = this.context
                context.putImageData(this.lastImageData, 0, 0)
                const [ ox, oy ] = this.circleOriginPoint
                const [ dx, dy ] = [ x - ox, y - oy ]
                const radius = Math.sqrt(dx * dx, dy * dy)
                context.lineWidth = this.size
                context.beginPath()
                context.arc((ox + x) / 2, (y + oy) / 2, radius, 0, 2 * Math.PI)
                if (this.fill === true) {
                    context.fillStyle = this.color2
                    context.fill()
                }
                if (this.border === true) {
                    context.strokeStyle = this.color1
                    context.stroke()
                }
                context.closePath()
                break
                case 'mouseup':
                this.circleOriginPoint = null
                this.lastImageData = null
                this.allImageData.push(this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT))
                //this.pointer += 1
                this.pointer = this.allImageData.length - 1
                break
            }
            this.socket.emit('drawing', {
                //imageData: this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT)
                type0: 'circle',
                action0: action,
                x0: x,
                y0: y,
                buttons0: buttons
            })
        },
        commandellipse (action, { x, y, buttons }) {
            switch (action) {
                case 'mousedown':
                this.circleOriginPoint = [x, y]
                this.lastImageData = this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT)
                break
                case 'mousemove':
                if (this.circleOriginPoint === null) {
                return
                }
                const context = this.context
                context.putImageData(this.lastImageData, 0, 0)
                const [ ox, oy ] = this.circleOriginPoint
                const [ dx, dy ] = [ x - ox, y - oy ]
                context.strokeStyle = this.color1
                context.lineWidth = this.size
                if (this.fill === true) {
                    context.fillStyle = this.color2
                }
                context.beginPath()
                context.ellipse((x + ox) / 2, (y + oy) / 2, dx / 2, dy / 2, 0, 0, 2 * Math.PI)
                if (this.fill === true) {
                    context.fillStyle = this.color2
                    context.fill()
                }
                if (this.border === true) {
                    context.strokeStyle = this.color1
                    context.stroke()
                }
                context.closePath()
                break
                case 'mouseup':
                this.circleOriginPoint = null
                this.lastImageData = null
                this.allImageData.push(this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT))
                //this.pointer += 1
                this.pointer = this.allImageData.length - 1
                break
            }
            this.socket.emit('drawing', {
                //imageData: this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT)
                type0: 'ellipse',
                action0: action,
                x0: x,
                y0: y,
                buttons0: buttons
            })
        }
    },

    mounted () {
        let emit = true
        if (this.operational) {
            ['mousemove', 'mousedown', 'mouseup'].map((eventName) => {
                this.$refs.board.addEventListener(eventName, ({ offsetX: x, offsetY: y, buttons }) => {
                    // this.$emit('action', this.type, eventName, { x, y, buttons, emit })
                    this[`command${this.type}`](eventName, { x, y, buttons } )
                })
            })
        }
        // this.$refs.board.addEventListener('mousedown', ({}))
        this.context = this.$refs.board.getContext('2d')
        this.allImageData.push(this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT))
        // socket.io
        let kkk = this
        this.socket = io.connect('http://localhost:9000')
        this.socket.on('drawing', function(data) {
            let x1 = data.x0
            let y1 = data.y0
            let buttons1 = data.buttons0
            // let emit1 = false
            // kkk.commandpenNotEmit(data.action0, { x1, y1, buttons1 })
            switch (data.type0) {
                case 'pen':
                if (data.action0 === 'mousedown') {
                    console.log(data.x0)
                    kkk.penOriginPoint = [data.x0, y1]
                    console.log(kkk.penOriginPoint)
                    kkk.lastImageData = kkk.context.getImageData(0, 0, kkk.WIDTH, kkk.HEIGHT)
                } else if (data.action0 === 'mousemove') {
                // console.log('mmm')
                    if (this.penOriginPoint === null) {
                        console.log('this.penOriginPoint === null')
                        return
                    }
                    const context = kkk.context
                    const [ ox, oy ] = kkk.penOriginPoint
                    context.strokeStyle = kkk.color1
                    context.lineWidth = kkk.size
                    context.beginPath()
                    context.moveTo(ox, oy)
                    context.lineTo(x1, y1)
                    context.stroke()
                    context.closePath()
                    kkk.penOriginPoint = [x1, y1]
                } else if (data.action0 === 'mouseup') {
                    kkk.penOriginPoint = null
                    kkk.lastImageData = null
                    kkk.allImageData.push(kkk.context.getImageData(0, 0, kkk.WIDTH, kkk.HEIGHT))
                    kkk.pointer = kkk.allImageData.length - 1
                }
                break
                case 'eraser':
                switch (data.action0) {
                    case 'mousedown':
                    kkk.circleOriginPoint = [x1, y1]
                    kkk.lastImageData = kkk.context.getImageData(0, 0, kkk.WIDTH, kkk.HEIGHT)
                    break
                    case 'mousemove':
                    if (kkk.circleOriginPoint === null) {
                        return
                    }
                    const context = kkk.context
                    const [ ox, oy ] = kkk.circleOriginPoint
                    context.clearRect(ox, oy, kkk.size * 10, kkk.size * 10)
                    kkk.circleOriginPoint = [x1, y1]
                    break
                    case 'mouseup':
                    kkk.circleOriginPoint = null
                    kkk.lastImageData = null
                    kkk.allImageData.push(kkk.context.getImageData(0, 0, kkk.WIDTH, kkk.HEIGHT))
                    //this.pointer += 1
                    kkk.pointer = kkk.allImageData.length - 1
                    break
                }
                break
                case 'line':
                switch (data.action0) {
                    case 'mousedown':
                    kkk.lineOriginPoint = [x1, y1]
                    kkk.lastImageData = kkk.context.getImageData(0, 0, kkk.WIDTH, kkk.HEIGHT)
                    break
                    case 'mousemove':
                    if (kkk.lineOriginPoint == null) {
                        return
                    }
                    const context = kkk.context
                    context.putImageData(kkk.lastImageData, 0, 0)
                    const [ ox, oy ] = kkk.lineOriginPoint
                    context.strokeStyle = kkk.color1
                    context.lineWidth = kkk.size
                    context.beginPath()
                    context.moveTo(ox, oy)
                    context.lineTo(x1, y1)
                    context.stroke()
                    context.closePath()
                    break
                    case 'mouseup':
                    kkk.lineOriginPoint = null
                    kkk.lastImageData = null
                    kkk.allImageData.push(kkk.context.getImageData(0, 0, kkk.WIDTH, kkk.HEIGHT))
                    //this.pointer += 1
                    kkk.pointer = kkk.allImageData.length - 1
                    break
                }
                break
                case 'rectangle':
                switch (data.action0) {
                    case 'mousedown':
                    kkk.circleOriginPoint = [x1, y1]
                    kkk.lastImageData = kkk.context.getImageData(0, 0, kkk.WIDTH, kkk.HEIGHT)
                    break
                    case 'mousemove':
                    if (kkk.circleOriginPoint === null) {
                    return
                    }
                    const context = kkk.context
                    context.putImageData(kkk.lastImageData, 0, 0)
                    const [ ox, oy ] = kkk.circleOriginPoint
                    const [ dx, dy ] = [ x1 - ox, y1 - oy ]
                    context.lineWidth = kkk.size
                    context.beginPath()
                    context.rect(ox, oy, dx, dy)
                    if (kkk.fill === true) {
                        context.fillStyle = kkk.color2
                        context.fill()
                    }
                    if (kkk.border === true) {
                        context.strokeStyle = kkk.color1
                        context.stroke()
                    }
                    context.closePath()
                    break
                    case 'mouseup':
                    kkk.circleOriginPoint = null
                    kkk.lastImageData = null
                    kkk.allImageData.push(kkk.context.getImageData(0, 0, kkk.WIDTH, kkk.HEIGHT))
                    //this.pointer += 1
                    kkk.pointer = kkk.allImageData.length - 1
                    break
                }
                break
                case 'circle':
                switch (data.action0) {
                    case 'mousedown':
                    kkk.circleOriginPoint = [x1, y1]
                    kkk.lastImageData = kkk.context.getImageData(0, 0, kkk.WIDTH, kkk.HEIGHT)
                    break
                    case 'mousemove':
                    if (kkk.circleOriginPoint === null) {
                        return
                    }
                    const context = kkk.context
                    context.putImageData(kkk.lastImageData, 0, 0)
                    const [ ox, oy ] = kkk.circleOriginPoint
                    const [ dx, dy ] = [ x1 - ox, y1 - oy ]
                    const radius = Math.sqrt(dx * dx, dy * dy)
                    context.lineWidth = kkk.size
                    context.beginPath()
                    context.arc((ox + x1) / 2, (y1 + oy) / 2, radius, 0, 2 * Math.PI)
                    if (kkk.fill === true) {
                        context.fillStyle = kkk.color2
                        context.fill()
                    }
                    if (kkk.border === true) {
                        context.strokeStyle = kkk.color1
                        context.stroke()
                    }
                    context.closePath()
                    break
                    case 'mouseup':
                    kkk.circleOriginPoint = null
                    kkk.lastImageData = null
                    kkk.allImageData.push(kkk.context.getImageData(0, 0, kkk.WIDTH, kkk.HEIGHT))
                    //this.pointer += 1
                    kkk.pointer = kkk.allImageData.length - 1
                    break
                }
                break
                case 'ellipse':
                switch (data.action0) {
                    case 'mousedown':
                    kkk.circleOriginPoint = [x1, y1]
                    kkk.lastImageData = kkk.context.getImageData(0, 0, kkk.WIDTH, kkk.HEIGHT)
                    break
                    case 'mousemove':
                    if (kkk.circleOriginPoint === null) {
                    return
                    }
                    const context = kkk.context
                    context.putImageData(kkk.lastImageData, 0, 0)
                    const [ ox, oy ] = kkk.circleOriginPoint
                    const [ dx, dy ] = [ x1 - ox, y1 - oy ]
                    context.strokeStyle = kkk.color1
                    context.lineWidth = kkk.size
                    if (kkk.fill === true) {
                        context.fillStyle = kkk.color2
                    }
                    context.beginPath()
                    context.ellipse((x1 + ox) / 2, (y1 + oy) / 2, dx / 2, dy / 2, 0, 0, 2 * Math.PI)
                    if (kkk.fill === true) {
                        context.fillStyle = kkk.color2
                        context.fill()
                    }
                    if (kkk.border === true) {
                        context.strokeStyle = kkk.color1
                        context.stroke()
                    }
                    context.closePath()
                    break
                    case 'mouseup':
                    kkk.circleOriginPoint = null
                    kkk.lastImageData = null
                    kkk.allImageData.push(kkk.context.getImageData(0, 0, kkk.WIDTH, kkk.HEIGHT))
                    //this.pointer += 1
                    kkk.pointer = kkk.allImageData.length - 1
                    break
                }
                break
                case 'clear':
                kkk.context.clearRect(0, 0, kkk.WIDTH, kkk.HEIGHT)
                kkk.allImageData.push(kkk.context.getImageData(0, 0, kkk.WIDTH, kkk.HEIGHT))
                kkk.pointer += 1
                break

            }
            console.log(data.action0)
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
