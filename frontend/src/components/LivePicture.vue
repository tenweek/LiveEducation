<template>
    <Card id="live-picture" padding="8">
        <div class="picture">
            <a @click="liveRoom">
                <div class="for-img">
                    <img :src="this.userImg" width="100%">
                </div>
                <label id="information-room-name">房间名:{{ this.roomName }}</label>
                <br>
                <label id="information-teacher-name">主讲教师:{{ this.teacherName }}</label>
                <label class="person">
                    <Icon type="person"></Icon>{{ this.studentNum }}
                </label>
            </a>
        </div>
    </Card>
</template>

<script>
/**
 * 表示正在直播房间的缩略图，
 * 包含老师上传的封面图片及房间信息（房间名称、老师名称、在线人数），
 * 作为子组件插入首页或直播详情页。
 *
 * @module LivePicture
 * @class LivePicture
 */
import myMsg from './../warning.js'
export default {
    name: 'live-picture',
    /**
     * 表示房间名称
     *
     * @property roomName
     */

    /**
     * 表示该直播房间老师名字
     *
     * @property teacherName
     */

    /**
     * 表示在线人数
     *
     * @property studentNum
     */

    /**
     * 表示房间id号
     *
     * @property id
     */

    /**
     * 表示该直播房间的缩略图
     *
     * @property userImg
     */
    props: ['roomName', 'teacherName', 'studentNum', 'id', 'userImg'],
    components: {
    },
    data: function () {
        return {}
    },
    /**
     * created函数，获取用户账号，
     * 判断该用户是否登录。
     *
     * @method created
     */
    methods: {
        /**
         * 获取房间信息
         *
         * @method liveRoom
         */
        liveRoom: function () {
            fetch('/joinRoom/', {
                method: 'post',
                mode: 'cors',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'roomID': this.id,
                })
            }).then((response) => response.json()).then((obj) => {
                if (obj.result === 'cannot') {
                    this.$Message.error(myMsg.room['cannotJoin'])
                } else if(obj.result==='login'){
                    this.$Message.error(myMsg.account['loginNeeded'])
                } else {
                    window.open('./#/live_room/' + this.id)
                }
            })
        }
    }
}
</script>

<style scoped>
.picture {
    width: 100%;
    height: 150px;
    margin-top: 10px;
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
