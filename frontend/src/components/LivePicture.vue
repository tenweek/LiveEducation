<template>
    <div class="picture">
        <a @click="liveRoom">
            <img src="../assets/papi.jpg" height="130">
            <label id="information-room-name">房间名:{{this.roomName}}</label>
            <br>
            <label id="information-teacher-name">主讲教师:{{this.teacherName}}</label>
            <label class="person">
                <Icon type="person"></Icon>{{this.studentNum}}</label>
        </a>
    </div>
</template>

<script>
export default {
    name: 'live-picture',
    props: ['roomName', 'teacherName', 'studentNum', 'id'],
    components: {
    },
    data: function () {
        return {
            canWork: false
        }
    },
    created: function () {
        let arrCookies = document.cookie.split(';')
        for (let i = 0; i < arrCookies.length; i++) {
            let arrStr = arrCookies[i].split('=')
            if (arrStr[0] === 'userAccount') {
                this.canWork = true
            }
        }
    },
    methods: {
        liveRoom: function () {
            if (this.canWork) {
                window.open('./#/live_room/')
            } else {
                this.$Message.error('请先登录！')
            }
        }
    }
}
</script>

<style scoped>
.picture {
    background: #efefef;
    width: 195px;
    height: 185px;
    margin-right: 30px;
    margin-left: 30px;
    margin-top: 15px;
    float: left;
    font-size: 14px;
    text-align: left;
}

#information-room-name {
    padding-left: 6px;
}

#information-teacher-name {
    padding-left: 5px;
}

.person {
    float: right;
    padding-right: 10px;
}

.picture a {
    color: #464c5b;
}

.picture:hover {
    color: #22313F;
}
</style>