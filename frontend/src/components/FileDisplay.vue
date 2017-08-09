<template>
    <div class="file-display">
        <img :src="this.route" width="680px" />
        <input type="button" value="pre" @click="prepicture" />
        <input type="button" value="next" @click="nextpicture" />
    </div>
</template>

<script src="/socket.io/socket.io.js"></script>
<script>
import * as io from 'socket.io-client'

export default {
    name: 'file-display',
    data: function () {
        return {
            roomid: '',
            socket: '',
            baseroute: '/static/img/',
            recroute: '',
            route: '',
            maxnum: '',
            nownum: ''
        }
    },
    created: function () {
        this.roomid = this.$route.params.id
        this.recroute = 'ppt/shili-'
        this.nownum = 1
        this.maxnum = 15
        this.route = this.baseroute+this.recroute+this.nownum+'.png'
        console.log(this.route)
    },
    methods: {
        nextpicture: function () {
            if (this.nownum < this.maxnum) {
                this.nownum = this.nownum + 1
                this.route = this.baseroute+this.recroute+this.nownum+'.png'
            }
        },
        prepicture: function () {
            if (this.nownum > 1) {
                this.nownum = this.nownum - 1
                this.route = this.baseroute+this.recroute+this.nownum+'.png'
            }
        }
    },
    mounted: function () {
        
    }
}
</script>