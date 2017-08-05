<template>
    <div class="picture">
        <a href="#" @click="live_room">
            <img src="../assets/papi.jpg" height="130">
            <label id="information-room-name">房间名</label>
            <br>
            <label id="information-teacher-name">主讲教师</label>
            <label class="person"><Icon type="person"></Icon>1234</label>
        </a>
    </div>
</template>

<script>
export default {
    name: 'live-picture',
    props:['roomname', 'username', 'id'],
    components: {
    },
    data: function () {
        return {
            roomid: this.id
        }
    },
    methods: {
        live_room: function () {
            window.open('./#/live_room/')
        }
    }
}
</script>

<style>
.picture {
    background: #efefef;
    width: 195px;
    height: 300px;
    margin-right: 30px;
    margin-left: 30px;
    margin-top: 15px;
    float: left;
    overflow: hidden;
    font-size: 14px;
}

#information-room-name {
    position: relative;
    left: -70px;
}
#information-teacher-name {
    position: relative;
    left: -43px;
}
.person {
    position: relative;
    left: 30px;
}
.picture a {
    color: #464c5b;
}

.picture:hover {
    color: #22313F;
}
</style>