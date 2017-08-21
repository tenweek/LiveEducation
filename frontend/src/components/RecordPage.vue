<template>
    <div class="record-page">
        <div class="header">
            <home-page-header :myOption="this.option"></home-page-header>
        </div>
        <div class="navigation">
            <div class="welcome">
                <Icon type="videocamera"></Icon>
                <label>录播课堂：</label>
            </div>
        </div>
        <div class="list">
            <div class="list-picture">
                <div v-for="room in rooms" class="every-picture">
                    <record-picture :roomName="room.roomName" :teacherName="room.teacherName" :liveId="room.liveId" :userImg="room.userImg"></record-picture class="record-picture">
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

.record-picture {
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

.record-page {
    background-color: #efefef;
    height: 50px;
}

.header {
    height: 60px;
    width: 100%;
    font-size: 40px;
    z-index: 50;
}
</style>
