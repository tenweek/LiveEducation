<template>
    <div class="picture">
        <a href="#" @click="live_room">
            <img src="../assets/papi.jpg" height="130">
            <label>房间名:</label><br>
            <label>主讲教师：</label><br>
            <label>在线人数：</label>
        </a>
    </div>
</template>

<script>
    export default {
        name: 'live-picture',
        components: {
        },
        data() {
            return {}
        },
        methods: {
            live_room(){
                window.open("http://localhost:8000/#/live_room/")
            }
        }
    }
</script>

<style>
    .picture{
        background: #efefef;
        width: 195px;
        height: 205px;
        margin-right: 30px;
        margin-left: 30px;
        margin-top: 15px;
        float: left;
        overflow: hidden;
        font-size: 14px;
        text-align: center;
    }
    .picture a{
        color: #464c5b;
    }
</style>