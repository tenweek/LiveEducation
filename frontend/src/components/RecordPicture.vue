<template>
    <div class="picture">
        <a @click="recordRoom">
            <img src="./../assets/record.jpg" height="130px">
            <label class="information">房间名</label>
            <br>
            <label class="information">&nbsp;&nbsp;主讲教师</label>
        </a>
    </div>
</template>

<script>
export default {
    name: 'RecordPicture',
    components: {},
    data: function () {
        return {
            canWork: false
        }
    },
    created: function () {
        let arrCookies = document.cookie.split(';')
        for (let i = 0; i < arrCookies.length; i++) {
            let arrStr = arrCookies[i].split('=')
            if (arrStr[0].replace(/(^\s*)|(\s*$)/g, '') === 'userAccount') {
                this.canWork = true
            }
        }
    },
    methods: {
        recordRoom: function () {
            if (this.canWork) {
                window.open('./#/record_room/')
            } else {
                this.$Message.error('请先登录！')
            }
        }
    }
}

</script>


<style scoped>
.picture {
    background: #efefef;
    width: 195px;
    height: 185px;
    margin-right: 30px;
    margin-left: 30px;
    margin-top: 15px;
    float: left;
    overflow: hidden;
    font-size: 14px;
}

.picture a {
    color: #464c5b;
}

.information {
    position: relative;
    right: 70px;
}

.picture:hover {
    color: #22313F;
}
</style>