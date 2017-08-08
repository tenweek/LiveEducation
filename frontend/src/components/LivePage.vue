<template>
    <div class="live-page">
        <div class="header">
            <home-page-header v-bind:myOption="option"></home-page-header>
        </div>
        <div class="navigation">
            <div class="welcome">
                <Icon type="university"></Icon>
                <label>当前正在直播：</label>
            </div>
        </div>

        <div class="list">
            <div class="list-picture">
                <live-picture v-for="room in rooms"
                    :roomName="room.roomName" :roomid="room.id" :teacherName="room.teacherName" :studentNum="room.studentNum">
                </live-picture>
            </div>
        </div>
        <div>
            <page-footer></page-footer>
        </div>
    </div>
</template>

<script>
import LivePicture from './LivePicture'
import HomePageHeader from './HomePageHeader'
import PageFooter from './PageFooter'

export default {
    name: 'live-page',
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
            rooms: [],
            option: 2
        }
    },
    methods: {
        getRooms: function () {
            fetch('getRooms', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'type': 2
                })
            }).then((response) => response.json()).then((obj) => {
                this.rooms = obj.rooms
            })
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.list {
    height: auto;
    min-height: 295px;
    width: 1100px;
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
    padding-top: 5px;
    padding-left: 35px;
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
    height: 60px;
    width: 100%;
    font-size: 40px;
    z-index: 9999;
}
</style>