<template>
    <div class="live-room">
        <div class="header">
            <home-page-header></home-page-header>
        </div>
        <div class="navigation">
            <div class="welcome">
                <Icon type="university"></Icon>
                <label>欢迎进入直播间 !</label>
            </div>
            <div class="navigation-center">
                <label class="information">房间ID：</label>
                <label class="information">房间名：</label>
                <label class="information">在线人数：</label>
            </div>
            <div class="navigation-right">
                <Button v-if="liveStatus === false" @click="status" type="default" shape="circle" size="small">开始直播</Button>
                <Button v-else @click="status" type="default" shape="circle" size="small">结束直播</Button>
            </div>
        </div>
        <div class="layout-header">
        </div>
    </div>
</template>

<script>
import LivePicture from './LivePicture'
import HomePageHeader from './HomePageHeader'

export default {
    name: 'hello',
    components: {
        LivePicture,
        HomePageHeader
    },
    data: function () {
        return {
            liveStatus: false
        }
    },
    methods: {
        status: function() {
            this.liveStatus = !this.liveStatus
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.live-room {
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
    background: #efefef;
    padding: 8px 10px;
    overflow: hidden;
    display: flex;
    font-size: 15px;
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

.information {
    margin: 0 auto;
}
</style>