<template>
    <Card id="record-picture" padding="8">
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
    </Card>
</template>

<script>
/**
 * 表示录播房间的缩略图，
 * 包含老师上传的封面图片及房间信息（房间名称、老师名称），
 * 作为子组件插入首页或录播详情页。
 *
 * @module RecordPicture
 * @class RecordPicture
 */
import myMsg from './../warning.js'
export default {
    name: 'RecordPicture',
    props: ['roomName', 'teacherName', 'userImg', 'liveId'],
    components: {},
    data: function () {
        return {
            /**
             *表示用户是否登录
             *
             * @attribute canWork
             * @type Boolean
             * @default false
             */
            canWork: false,
            route: ''
        }
    },
    /**
     * created函数，判断用户是否登录
     *
     * @method created
     */
    created: function () {
        let arrCookies = document.cookie.split(';')
        for (let i = 0; i < arrCookies.length; i++) {
            let arrStr = arrCookies[i].split('=')
            if (arrStr[0].replace(/(^\s*)|(\s*$)/g, '') === 'userAccount') {
                this.canWork = true
            }
        }
        this.route = '/static/cover/' + this.userImg
    },
    methods: {
        /**
         * 进入录播房间，
         * 如果用户没有登录，则弹出消息框提示。
         *
         * @method recordRoom
         */
        recordRoom: function () {
            if (this.canWork) {
                window.open('./#/record_room/' + this.liveId)
            } else {
                this.$Message.error(myMsg.account['loginNeeded'])
            }
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
    height: auto;
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
