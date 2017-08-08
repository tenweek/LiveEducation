<template>
    <div class="head-bg">
        <div class="header">
            <home-page-header v-bind:myOption="option"></home-page-header>
        </div>
        <div class="navigation">
            <div class="welcome">
                <Icon type="videocamera"></Icon>
                <label>录播课堂：</label>
            </div>
        </div>
        <div class="list">
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
                <record-picture></record-picture>
            </div>
        </div>
        <div>
            <page-footer></page-footer>
        </div>
    </div>
</template>

<script>
import RecordPicture from './RecordPicture'
import HomePageHeader from './HomePageHeader'
import PageFooter from './PageFooter'

export default {
    name: 'record-page',
    components: {
        RecordPicture,
        HomePageHeader,
        PageFooter
    },
    data: function () {
        return {
            option: 3
        }
    },
    methods: {
    }
}
</script>

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
    display: flex;
    font-size: 15px;
}

.head-bg {
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