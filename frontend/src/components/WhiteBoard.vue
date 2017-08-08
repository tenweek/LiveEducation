<template>
    <div class="white-board">
        <div class="tools">
<<<<<<< HEAD
            <button :class="{ active: type === 'pen'}" @click="type = 'pen'"><Icon type="edit"></Icon></button>
=======
            <button :class="{ active: type === 'pen'}" @click="type = 'pen'">铅笔</button>
>>>>>>> 0f2de92282b520c30c1d929784c8d876d01ca2bf
            <button :class="{ active: type === 'text'}" @click="type = 'text'">文字</button>
            <button :class="{ active: type === 'eraser'}" @click="type = 'eraser'">橡皮擦</button>
            <button :class="{ active: type === 'line'}" @click="type = 'line'">直线</button>
            <button :class="{ active: type === 'rectangle'}" @click="type = 'rectangle'">矩形</button>
            <button :class="{ active: type === 'circle'}" @click="type = 'circle'">圆形</button>
            <button :class="{ active: type === 'ellipse'}" @click="type = 'ellipse'">椭圆</button>
<<<<<<< HEAD
            <el-color-picker v-model="color" show-alpha></el-color-picker>
=======
>>>>>>> 0f2de92282b520c30c1d929784c8d876d01ca2bf
        </div>
        <div class="drawing-board">
            <canvas ref="board" class="canvas" :width="WIDTH" :height="HEIGHT"></canvas>
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
            color: 'rgba(19, 206, 102, 0.8)'
        }
    },
    methods: {
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
                //context.putImageData(this.lastImageData, 0, 0)
                const [ ox, oy ] = this.penOriginPoint
                context.beginPath()
                context.moveTo(ox, oy)
                context.lineTo(x, y)
                context.stroke()
                context.closePath()
                this.penOriginPoint = [x, y]
                //context.putImageData(this.lastImageData, 0, 0)
                break
                case 'mouseup':
                this.penOriginPoint = null
                this.lastImageData = null
                break
            }
        },

        commandtext(action, { x, y, buttons }) {
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
            //context.putImageData(this.lastImageData, 0, 0)
            const [ ox, oy ] = this.circleOriginPoint
            //context.clearRect(ox, oy, 10, 10)
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
            //context.putImageData(this.lastImageData, 0, 0)
            const [ ox, oy ] = this.circleOriginPoint
            context.clearRect(ox, oy, 10, 10)

            this.circleOriginPoint = [x, y]
            break
            case 'mouseup':
            this.circleOriginPoint = null
            this.lastImageData = null
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
                context.beginPath()
                context.moveTo(ox, oy)
                context.lineTo(x, y)
                context.stroke()
                context.closePath()
                break
                case 'mouseup':
                this.lineOriginPoint = null
                this.lastImageData = null
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
                context.beginPath()
                context.rect(ox, oy, dx, dy)
                context.stroke() // 通过线条来绘制图形轮廓
                //context.fill() // 通过填充路径的内容区域生成实心的图形
                context.closePath()
                break
                case 'mouseup':
                this.circleOriginPoint = null
                this.lastImageData = null
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
                context.beginPath()
                context.arc((ox + x)/2, (y + oy)/2, radius, 0, 2 * Math.PI)
                context.stroke() // 通过线条来绘制图形轮廓
                //context.fill() // 通过填充路径的内容区域生成实心的图形
                context.closePath()
                break
                case 'mouseup':
                this.circleOriginPoint = null
                this.lastImageData = null
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
                context.beginPath()
                // ************************************************！！！括号、/ 空格问题
                context.ellipse((x + ox)/2, (y + oy)/2, dx/2, dy/2, 0, 0, 2 * Math.PI)
                context.stroke() // 通过线条来绘制图形轮廓
                //context.fill() // 通过填充路径的内容区域生成实心的图形
                context.closePath()
                break
                case 'mouseup':
                this.circleOriginPoint = null
                this.lastImageData = null
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
    this.context = this.$refs.board.getContext('2d')
  }
}
</script>

<style scoped>

.white-board {
    height: 100%;
    display: flex;
}

.tools {
    height: auto;
    width: 85px;
    background: #99ff99;
}

button {
    background-color: #ccc;
    height: 37px;
    width: 37px;
    margin-left: 0;
    margin-right: 0;
}

button.active {
    background-color: #aaa;
}

.drawing-board {
    height: 100%;
    width: 100%;
}

.canvas {
    background: white;
}

</style>
