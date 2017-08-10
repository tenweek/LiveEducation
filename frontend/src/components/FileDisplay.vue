<template>
    <div class="file-display" id="file" @click="makefoucs" @keydown="modpicture()" tabindex="0">
        <img :src="this.route" width="675px" class="my-img" />
    </div>
</template>

<script>

export default {
    name: 'file-display',
    data: function () {
        return {
            roomid: '',
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
        },
        modpicture: function () {
            if (event.keyCode === 39 || event.keyCode === 40) {
                this.nextpicture()
            }
            if (event.keyCode === 37 || event.keyCode === 38) {
                this.prepicture()
            }
        },
        makefoucs: function () {
            var linshi = document.getElementById('file')
            linshi.focus(); 
        }
    }
}
</script>

<style scoped>
.my-img {
    border: 3px solid #000;
}
.file-display {
    width: 680px;
    height: 480px;
}
</style>