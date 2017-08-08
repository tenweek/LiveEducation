<template>
    <div class="white-board">
        <div class="tools">
            <div class="undo-redo">
                <Button type="text" class="button-undo-redo" @click="undo"><Icon type="reply"></Icon></Button>
                <Button type="text" class="button-undo-redo" @click="redo"><Icon type="forward"></Icon></Button>
            </div>
            <Button type="text" class="clear" @click="clear">清空</Button>
            <Button type="text" :class="{ active: type === 'eraser' }" @click="type = 'eraser'">橡皮擦</Button>
            <Button type="text" :class="{ active: type === 'pen' }" @click="type = 'pen'"><Icon type="edit"></Icon>&nbsp;&nbsp;铅笔</Button>
            <Button type="text" :class="{ active: type === 'text' }" @click="type = 'text'">文字</Button>
            <Button type="text" :class="{ active: type === 'line' }" @click="type = 'line'">直线</Button>
            <Button type="text" :class="{ active: type === 'rectangle' }" @click="type = 'rectangle'">矩形</Button>
            <Button type="text" :class="{ active: type === 'circle' }" @click="type = 'circle'">圆形</Button>
            <Button type="text" :class="{ active: type === 'ellipse' }" @click="type = 'ellipse'">椭圆</Button>
            <Button type="text" :class="{ active: border === true }" @click="border = !border">边框</Button>
            <el-color-picker class="color-selected" v-model="color1" show-alpha>颜色1</el-color-picker>
            <Button type="text" :class="{ active: fill === true }" @click="fill = !fill">填充</Button>
            <el-color-picker class="color-selected" v-model="color2" show-alpha></el-color-picker>
            <div class="size">
                <Button type="text" :class="{ active: size === 5 }" id="button-size" @click="size = 5">大</Button>
                <Button type="text" :class="{ active: size === 3 }" id="button-size" @click="size = 3">中</Button>
            </div>
            <Button type="text" :class="{ active: size === 1 }" id="button-size" @click="size = 1">小</Button>
        </div>

        <div class="drawing-board">
            <canvas ref="board" class="canvas" :width="WIDTH" :height="HEIGHT">
                <label v-show="textField === true">Hello</label>
            </canvas>
        </div>
    </div>
</template>

<script>
export default {
    name: 'white-board',
    props: {
        operational: {
            type: Boolean,
            default: true
        }
    },
    data() {
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
            textField: true,
            allImageData: [],
            pointer: 0
        }
    },
    methods: {
        clear() {
            this.context.clearRect(0, 0, this.WIDTH, this.HEIGHT)
            this.allImageData.push(this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT))
            this.pointer += 1
            if(this.allImageData != null) {
                alert(this.allImageData)
                alert(this.pointer)
            }
            return
        },

        undo() {
            if (this.pointer != 0) {
                this.pointer -= 1
            }
            this.context.putImageData(this.allImageData[this.pointer-1], 0, 0)
        },

        commandpen(action, { x, y, buttons }) {
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
                    this.pointer += 1
                    if(this.allImageData != null) {
                        alert(this.allImageData)
                    }
                    break
            }
        },

        commandtext(action, { x, y, buttons }) {
            switch (action) {
                case 'mousedown':
                    this.textField = true
                    this.circleOriginPoint = [x, y]
                    this.lastImageData = this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT)
                    break
            case 'mousemove':
                if (this.circleOriginPoint === null) {
                    return
                }
                const context = this.context
                const [ ox, oy ] = this.circleOriginPoint
                context.fillText("Hello World", ox, oy)
                this.circleOriginPoint = [x, y]
                break
            case 'mouseup':
                this.circleOriginPoint = null
                this.lastImageData = null
                break
            }
        },

        commanderaser(action, { x, y, buttons }) {
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
                context.clearRect(ox, oy, this.size*10, this.size*10)

                this.circleOriginPoint = [x, y]
                break
            case 'mouseup':
                this.circleOriginPoint = null
                this.lastImageData = null
                this.allImageData.push(this.context.getImageData(0, 0, this.WIDTH, this.HEIGHT))
                this.pointer += 1
                if(this.allImageData != null) {
                    alert(this.allImageData)
                    alert(this.pointer)
                }
                break
            }
        },

        commandline(action, { x, y, buttons }) {
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
                    this.pointer += 1
                    if(this.allImageData != null) {
                        alert(this.allImageData)
                        alert(this.pointer)
                    }
                    break
            }
        },

        commandrectangle(action, {x, y, buttons }) {
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
                    this.pointer += 1
                    if(this.allImageData != null) {
                        alert(this.allImageData)
                        alert(this.pointer)
                    }
                    break
            }
        },

        commandcircle(action, { x, y, buttons }) {
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
                    context.arc((ox + x)/2, (y + oy)/2, radius, 0, 2 * Math.PI)
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
                    this.pointer += 1
                    if(this.allImageData != null) {
                        alert(this.allImageData)
                        alert(this.pointer)
                    }
                    break
            }
        },
        commandellipse(action, { x, y, buttons }) {
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
                    context.ellipse((x + ox)/2, (y + oy)/2, dx/2, dy/2, 0, 0, 2 * Math.PI)
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
                    this.pointer += 1
                    if(this.allImageData != null) {
                        alert(this.allImageData)
                        alert(this.pointer)
                    }
                    break
            }
        }
    },

    mounted() {
        if (this.operational) {
            ['mousemove', 'mousedown', 'mouseup'].map((eventName) => {
                this.$refs.board.addEventListener(eventName, ({ offsetX: x, offsetY: y, buttons }) => {
                this.$emit('action', this.type, eventName, { x, y, buttons })
                this[`command${this.type}`](eventName, { x, y, buttons })
                })
            })
        }
        this.context = this.$refs.board.getContext('2d')
    }
  }
</script>

<style scoped>

.undo-redo {
    display: flex;
}

.button-undo-redo {
    width: 37px;
}

.button-undo-redo:hover {
    border: 1.5px solid yellow;
}

.clear:hover {
    border: 1.5px solid yellow;
}

.white-board {
    height: 100%;
    display: flex;
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

#button-size {
    width: 37px;
}

.drawing-board {
    height: 100%;
    width: 100%;
}

.canvas {
    background: white;
}

</style>
