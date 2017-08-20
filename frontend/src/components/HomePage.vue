<template>
    <div class="home-page">
        <div class="header">
            <home-page-header :myOption="this.option"></home-page-header>
        </div>
        <div class="list">
            <div class="list-hint">
                <Icon type="university" class="icon-middle"></Icon>
                <input type="text" class="live-broadcast" value="直播课堂" readonly="true" ></input>
                <a href="#/live_page" class="more">查看更多
                        <Icon type="chevron-right"></Icon>
                </a>
            </div>
            <div class="list-picture">
                <div  v-for="room in rooms" class="every-picture">
                    <live-picture :roomName="room.roomName" :id="room.id" :teacherName="room.teacherName" :studentNum="room.studentNum" :userImg="room.userImg" class="live-picture">
                    </live-picture>
                </div>
            </div>
        </div>
        <div class="list">
            <div class="list-hint">
                <Icon type="university" class="icon-middle"></Icon>
                <input type="text" class="live-broadcast" value="录播课堂" readonly="true" ></input>
                <a href="#/record_page" class="more">查看更多
                        <Icon type="chevron-right"></Icon>
                </a>
            </div>
            <div class="list-picture">
                <div class="every-picture">
                    <record-picture></record-picture>
                </div>
                <div class="every-picture">
                    <record-picture></record-picture>
                </div>
                 <div class="every-picture">
                    <record-picture></record-picture>
                </div>
                <div class="every-picture">
                    <record-picture></record-picture>
                </div>
                 <div class="every-picture">
                    <record-picture></record-picture>
                </div>
                <div class="every-picture">
                    <record-picture></record-picture>
                </div>
                 <div class="every-picture">
                    <record-picture></record-picture>
                </div>
                <div class="every-picture">
                    <record-picture></record-picture>
                </div>
            </div>
        </div>
        <div>
            <page-footer></page-footer>
        </div>
    </div>
</template>

<script>
/**
 * 直播网站的首页，
 * 包含导航栏、直播列表、录播列表等信息
 *
 * @modules HomePage
 * @class HomePage
 */
import LivePicture from './LivePicture'
import RecordPicture from './RecordPicture'
import HomePageHeader from './HomePageHeader'
import PageFooter from './PageFooter'

export default {
    name: 'home-page',
    components: {
        LivePicture,
        RecordPicture,
        HomePageHeader,
        PageFooter
    },
    data: function () {
        return {
            /**
             * 存储所有房间信息
             *
             * @attribute rooms
             * @type Array
             * @default []
             */
            rooms: [],
            /**
             * 表示导航栏的选择（首页、直播、录播）
             *
             * @attribute option
             * @type Number
             * @default 1 1表示当前处于首页
             */
            option: 1
        }
    },
    /**
     * created函数，调用getRooms函数，
     * 获取房间信息
     *
     * @method created
     */
    created: function () {
        this.getRooms()
    },
    methods: {
        /**
         * 获取正在直播及录播房间信息
         *
         * @method getRooms
         */
        getRooms: function () {
            fetch('/getRooms/', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ 'type': 1 })
            }).then((response) => response.json()).then((obj) => {
                this.rooms = obj.rooms
            })
        }
    }
}
</script>

<style scoped>
.home-page {
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 5px;
    overflow: hidden;
}

.header {
    height: 60px;
    width: 100%;
    font-size: 40px;
}

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
}

.live-picture {
    width: 100%;
    height: auto;
    margin: auto;
}

.list-hint {
    height: 45px;
    line-height: 45px;
    width: 100%;
    font-size: 25px;
    padding-left: 20px;
    padding-right: 20px;
    border-bottom: solid;
}

.icon-middle {
    float: left;
    margin-top: 10px;
}

.live-broadcast {
    width: 150px;
    height: 40px;
    border: none;
    float: left;
    margin-left: 10px;
}

.more {
    font-size: 15px;
    float: right;
    color: #464c5b;
    height: 30px;
    padding-top: 10px;
}

.layout-logo {
    width: 100px;
    height: 30px;
    background: #5b6270;
    border-radius: 5px;
    float: left;
    position: relative;
    top: 15px;
    left: 20px;
}
</style>