<template>
    <div class="live-page">
        <div class="header">
            <home-page-header :myOption="this.option"></home-page-header>
        </div>
        <Card id="live-list" padding="0" dis-hover>
            <div class="list">
                <div class="list-hint">
                    <input type="text" class="live-broadcast" value="直播课堂" readonly="true"></input>
                </div>
                <div class="list-picture">
                    <div v-for="room in rooms" class="every-picture">
                        <live-picture :roomName="room.roomName" :id="room.id" :teacherName="room.teacherName" :studentNum="room.studentNum" :userImg="room.userImg" class="live-picture">
                        </live-picture>
                    </div>
                </div>
            </div>
        </Card>
        <div>
            <page-footer></page-footer>
        </div>
        <Back-top></Back-top>
    </div>
</template>

<script>
/**
 * 直播详情页，
 * 包含正在直播的所有房间缩略图及信息。
 *
 * @module LivePage
 * @class LivePage
 */
import LivePicture from './LivePicture'
import HomePageHeader from './HomePageHeader'
import PageFooter from './PageFooter'

export default {
    name: 'live-page',
    /**
     * created函数，调用getRooms函数
     *
     * @method created
     */
    created: function () {
        this.getRooms()
    },
    components: {
        LivePicture,
        HomePageHeader,
        PageFooter
    },
    data: function () {
        return {
            /**
             * 表示导航栏的选择（首页、直播、录播）
             *
             * @attribute option
             * @type Number
             * @default 2 2表示当前处于直播详情页
             */
            option: 2,
            /**
             * 存储所有正在直播的房间信息
             *
             * @attribute rooms
             * @type Array
             * @default []
             */
            rooms: []
        }
    },
    methods: {
        /**
         * 获取房间信息
         *
         * @method getRooms
         */
        getRooms: function () {
            fetch('/getRooms/', {
                method: 'post',
                mode: 'cors',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ 'type': 2 })
            }).then((response) => response.json()).then((obj) => {
                this.rooms = obj.rooms
            })
        }
    }
}
</script>

<style scoped>
#live-list {
    height: auto;
    min-height: 295px;
    width: 85%;
    min-width: 800px;
    max-width: 1200px;
    margin: auto;
    margin-bottom: 40px;
    margin-top: 40px;
    overflow: hidden;
    background: white;
}

.list-picture {
    height: 100%;
    width: 100%;
    min-width: 800px;
    padding-top: 5px;
    padding-left: 4%;
    padding-bottom: 16px;
    margin: auto;
    display: flex;
    flex-wrap: wrap;
}

.list-hint {
    height: 61px;
    line-height: 45px;
    margin: auto;
    width: 96%;
    font-size: 25px;
    padding-left: 20px;
    padding-right: 20px;
    padding-top: 16px;
    border-bottom: solid #e9eaec 1px;
    margin: auto;
}

.every-picture {
    margin: 10px 10px;
}

.live-picture {
    width: 100%;
    height: auto;
    margin: auto;
}

.live-broadcast {
    width: 150px;
    height: 30px;
    margin-top: 12px;
    font-size: 25px;
    border: none;
    float: left;
    margin-left: 6px;
}

.live-page {
    background-color: #f4f4f4;
    position: relative;
    overflow: hidden;
}

.header {
    height: 50px;
    width: 100%;
    font-size: 40px;
}
</style>
