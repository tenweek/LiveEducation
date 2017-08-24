<template>
    <div class="home-page">
        <div class="header">
            <home-page-header :myOption="this.option"></home-page-header>
        </div>
        <Card id="live-list" padding="0" dis-hover>
            <div class="list">
                <div class="list-hint">
                    <input type="text" class="live-broadcast" value="直播课堂" readonly="true"></input>
                    <a href="#/live_page" class="more">查看更多
                        <Icon type="chevron-right"></Icon>
                    </a>
                </div>
                <div class="list-picture">
                    <div v-for="room in rooms" class="every-picture">
                        <live-picture :roomName="room.roomName" :id="room.id" :teacherName="room.teacherName" :studentNum="room.studentNum" :userImg="room.userImg" class="live-picture">
                        </live-picture>
                    </div>
                </div>
            </div>
        </Card>
        <Card id="record-list" padding="0" dis-hover>
            <div class="list">
                <div class="list-hint">
                    <input type="text" class="live-broadcast" value="录播课堂" readonly="true"></input>
                    <a href="#/record_page" class="more">查看更多
                        <Icon type="chevron-right"></Icon>
                    </a>
                </div>
                <div class="list-picture">
                    <div v-for="videoRoom in videoRooms" class="every-picture">
                        <record-picture :roomName="videoRoom.roomName" :teacherName="videoRoom.teacherName" :liveId="videoRoom.liveId" :userImg="videoRoom.userImg"></record-picture>
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
 * 直播网站的首页，
 * 包含导航栏、直播列表、录播列表等信息
 *
 * @module HomePage
 * @class HomePage
 */
import LivePicture from './LivePicture'
import RecordPicture from './RecordPicture'
import HomePageHeader from './HomePageHeader'
import PageFooter from './PageFooter'

export default {
    name: 'home-page',
    created: function () {
        this.getRooms()
        this.getVideoRooms()
    },
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
            videoRooms: [],
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
    methods: {
        getVideoRooms: function () {
            fetch('/getVideoRooms/', {
                method: 'post',
                mode: 'cors',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ 'type': 1 })
            }).then((response) => response.json()).then((obj) => {
                this.videoRooms = obj.rooms
            })
        },
        /**
         * 获取正在直播及录播房间信息
         *
         * @method getRooms
         */
        getRooms: function () {
            fetch('/getRooms/', {
                method: 'post',
                credentials: 'same-origin',
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
    position: relative;
    overflow: hidden;
    background-color: #f4f4f4;
}

.header {
    height: 50px;
    width: 100%;
    font-size: 40px;
}

#live-list,
#record-list {
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

.more {
    font-size: 15px;
    float: right;
    color: #999;
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
