<template>
    <div class="record-page">
        <div class="header">
            <home-page-header :myOption="this.option"></home-page-header>
        </div>
        <Card id="record-list" padding="0" dis-hover>
            <div class="list">
                <div class="list-hint">
                    <input type="text" class="live-broadcast" value="录播课堂" readonly="true"></input>
                </div>
                <div class="list-picture">
                    <div v-for="room in rooms" class="every-picture">
                        <record-picture :roomName="room.roomName" :teacherName="room.teacherName" :liveId="room.liveId" :userImg="room.userImg"></record-picture class="record-picture">
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
 * 录播详情页，显示所有录播房间的缩略图及房间信息。
 *
 * @module RecordPage
 * @class RecordPage
 */
import RecordPicture from './RecordPicture'
import HomePageHeader from './HomePageHeader'
import PageFooter from './PageFooter'

export default {
    name: 'record-page',
    created: function () {
        this.getVideoRooms()
    },
    components: {
        RecordPicture,
        HomePageHeader,
        PageFooter
    },
    /**
     * 表示导航栏的选择（首页、直播、录播）
     *
     * @attribute option
     * @type Number
     * @default 3 3表示当前处于录播详情页
     */
    data: function () {
        return {
            option: 3,
            rooms: []
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
                body: JSON.stringify({ 'type': 2 })
            }).then((response) => response.json()).then((obj) => {
                this.rooms = obj.rooms
            })
        }
    }
}
</script>

<style scoped>
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

.record-picture {
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

.record-page {
    background-color: #f4f4f4;
    position: relative;
    overflow: hidden;
}

.header {
    height: 50px;
    width: 100%;
    font-size: 40px;
    z-index: 50;
}
</style>
