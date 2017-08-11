<template>
    <div class="home-page">
        <div class="header">
            <home-page-header :myOption="this.option"></home-page-header>
        </div>
        <div class="list">
            <div class="list-hint">
                <div class="icon">
                    <Icon type="university" class="icon-middle"></Icon>
                </div>
                &nbsp;
                <label class="live-broadcast">正在直播</label>
                <a href="#/live_page" class="more">
                    <b>
                        <label>查看更多
                            <Icon type="chevron-right"></Icon>
                        </label>
                    </b>
                </a>
            </div>
            <div class="list-picture">
                <live-picture v-for="room in rooms" :roomName="room.roomName" :id="room.id" :teacherName="room.teacherName" :studentNum="room.studentNum">
                </live-picture>
            </div>
        </div>
        <div class="list">
            <div class="list-hint">
                <div class="icon">
                    <Icon type="videocamera" class="icon-middle"></Icon>
                </div>
                &nbsp;
                <label class="live-broadcast">录播课堂</label>
                <a href="#/record-page" class="more">
                    <b>
                        <label>查看更多
                            <Icon type="chevron-right"></Icon>
                        </label>
                    </b>
                </a>
            </div>
            <div class="list-picture">
                <record-picture></record-picture>
                <record-picture></record-picture>
                <record-picture></record-picture>
                <record-picture></record-picture>
                <record-picture></record-picture>
                <record-picture></record-picture>
                <record-picture></record-picture>
                <record-picture></record-picture>
                <record-picture></record-picture>
            </div>
        </div>
        <div>
            <page-footer></page-footer>
        </div>
    </div>
</template>

<script>
import LivePicture from './LivePicture'
import RecordPicture from './RecordPicture'
import HomePageHeader from './HomePageHeader'
import PageFooter from './PageFooter'

export default {
    name: 'home-page',
    created: function () {
        this.getRooms()
    },
    components: {
        LivePicture,
        RecordPicture,
        HomePageHeader,
        PageFooter
    },
    data: function () {
        return {
            rooms: [],
            option: 1
        }
    },
    methods: {
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
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

.navigation {
    background: #464c5b;
    padding: 8px 0;
    overflow: hidden;
    display: flex;
}

.navigation-center {
    margin: 0 auto;
    font-size: 15px;
}

.navigation-right {
    float: right;
    margin-right: 15px;
    font-size: 15px;
}

.navigation-bar:hover {
    color: gold;
}

.navigation a {
    color: #9ba7b5;
}

.list {
    height: auto;
    height: auto;
    min-height: 295px;
    width: 1100px;
    background: #fff;
    box-shadow: 0 1px 1px rgba(0, 0, 0, .1);
    margin: auto;
    overflow: hidden;
    background: white;
    padding-top: 8px;
}

.list-picture {
    height: 100%;
    padding-top: 5px;
    padding-left: 35px;
}

.list-hint {
    height: 45px;
    line-height: 45px;
    width: 100%;
    font-size: 25px;
    display: flex;
    padding-left: 20px;
    padding-right: 20px;
    border-bottom: solid;
}

.more {
    float: right;
    font-size: 15px;
    color: #464c5b;
    padding-top: 4px;
    margin-left: 850px;
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

.footer {
    text-align: center;
    padding: 5px 0 5px;
    color: #9ea7b4;
}
</style>