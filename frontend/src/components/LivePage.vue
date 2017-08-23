<template>
    <div class="live-page">
        <div class="header">
            <home-page-header :myOption="this.option"></home-page-header>
        </div>
        <div class="navigation">
            <div class="welcome">
                <Icon type="university"></Icon>
                <label>当前正在直播：</label>
            </div>
        </div>
        <div class="list">
            <div v-for="room in rooms" class="every-picture">
                <live-picture :roomName="room.roomName" :id="room.id" :teacherName="room.teacherName" :studentNum="room.studentNum" :userImg="room.userImg" class="live-picture">
                </live-picture>
            </div>
        </div>
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
.list {
    height: auto;
    min-height: 295px;
    width: 65%;
    min-width: 800px;
    max-width: 1000px;
    background: #fff;
    box-shadow: 0 1px 1px rgba(0, 0, 0, .1);
    margin: auto;
    overflow: hidden;
    background: white;
    padding-top: 8px;
    padding-bottom: 30px;
    display: flex;
    flex-wrap: wrap;
}

.list-picture {
    height: 100%;
    width: 100%;
    min-width: 800px;
    padding-top: 5px;
    padding-left: 4%;
    margin: auto;
    display: flex;
    flex-wrap: wrap;
}

.every-picture {
    width: 20%;
    margin-left: 2%;
    margin-right: 2%;
    margin-top: 10px;
}

.live-picture {
    width: 160px;
    height: auto;
    margin: auto;
}

.navigation {
    background: #efefef;
    padding: 8px 40px;
    overflow: hidden;
    display: flex;
    font-size: 15px;
}


.live-page {
    background-color: #efefef;
    height: 50px;
}

.header {
    height: 50px;
    width: 100%;
    font-size: 40px;
    z-index: 50;
}
</style>
