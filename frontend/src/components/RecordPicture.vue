<template>
    <div class="picture">
        <a @click="recordRoom">
            <div class="for-img">
                <img :src="this.route" width="100%">
            </div>
            <label id="information-room-name">房间名:{{ this.roomName }}</label>
            <br>
            <label id="information-teacher-name">主讲教师: {{ this.teacherName }}</label>
        </a>
    </div>
</template>

<script>
import myMsg from './../warning.js'
export default {
    name: 'RecordPicture',
    props: ['roomName', 'teacherId', 'teacherName', 'liveId', 'userImg', 'videoId'],
    components: {},
    data: function () {
        return {
            canWork: false,
            route: ''
        }
    },
    created: function () {
        let arrCookies = document.cookie.split(';')
        for (let i = 0; i < arrCookies.length; i++) {
            let arrStr = arrCookies[i].split('=')
            if (arrStr[0].replace(/(^\s*)|(\s*$)/g, '') === 'userAccount') {
                this.canWork = true
            }
        }
        this.route = "/static/cover/" + this.userImg
    },
    methods: {
        recordRoom: function () {
            if (this.canWork) {
                window.open('./#/record_room/' + this.videoId)
            } else {
                this.$Message.error(myMsg.account['loginNeeded'])
            }
        }
    }
}

</script>

<style scoped>
.picture {
    background: #efefef;
    width: 160px;
    height: 150px;
    margin-top: 15px;
    font-size: 14px;
    text-align: left;
}

.for-img {
    width: 100%;
    height: 105px;
}

#information-room-name {
    padding-left: 6px;
}

#information-teacher-name {
    padding-left: 5px;
}

.picture a {
    color: #464c5b;
}

.picture:hover {
    color: #22313F;
}
</style>