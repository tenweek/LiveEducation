<template>
    <div class="record-room">
        <div class="header">
            <home-page-header></home-page-header>
        </div>
        <div class="navigation">
            <div class="welcome">
                <Icon type="videocamera"></Icon>
                <label>欢迎观看录播！</label>
            </div>
            <div class="navigation-center">
                <label class="information">录播ID：</label>
                <label class="information">录播名：</label>
            </div>
        </div>
        <div class="layout-header">
            <video-display></video-display>
        </div>
        <div>
            <page-footer></page-footer>
        </div>
    </div>
</template>

<script>
import VideoDisplay from './VideoDisplay'
import PageFooter from './PageFooter'
import HomePageHeader from './HomePageHeader'

export default {
    name: 'record-room',
    components: {
        VideoDisplay,
        PageFooter,
        HomePageHeader
    },
    data: function () {
        return {}
    }
}
</script>

<style scoped>
.record-room {
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

.layout-header {
    width: 1100px;
    height: 490px;
    display: flex;
    margin-left: auto;
    margin-right: auto;
    margin-top: 20px;
    border: solid;
}
</style>