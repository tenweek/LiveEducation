<template>
    <div class="picture">
        <a @click="recordRoom">
            <div class="for-img">
                <img src="./../assets/record.jpg" width="100%">
            </div>
            <label id="information-room-name">房间名</label>
            <br>
            <label id="information-teacher-name">主讲教师</label>
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
    width: 160px;
    height: 150px;
    margin-top: 15px;
    font-size: 14px;
    text-align: left;
}

.for-img {
    width: 100%;
    height: 105px;
}

#information-room-name {
    padding-left: 6px;
}

#information-teacher-name {
    padding-left: 5px;
}

.picture a {
    color: #464c5b;
}

.picture:hover {
    color: #22313F;
}
</style>