<template>
    <div class="picture">
        <a href="#" @click="recordRoom">
            <img src="../assets/record.jpg" height="130">
            <label>&nbsp;&nbsp;房间名</label>
            <br>
            <label>&nbsp;&nbsp;主讲教师</label>
        </a>
    </div>
</template>

<script>
export default {
    name: 'live-picture',
    components: {
    },
    data: function () {
        return {}
    },
    methods: {
        recordRoom: function () {
            window.open('./#/record_room/')
        }
    }
}
</script>

<style>
.picture {
    background: #efefef;
    width: 195px;
    height: 205px;
    margin-right: 30px;
    margin-left: 30px;
    margin-top: 15px;
    float: left;
    overflow: hidden;
    font-size: 14px;
}
.picture a {
    color: #464c5b;
}

.picture:hover {
    color: #22313F;
}
</style>