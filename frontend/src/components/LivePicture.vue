<template>
    <div class="picture">
        <a @click="liveRoom">
            <div class="for-img">
                <img src="../assets/papi.jpg" width="100%">
            </div>
            <label id="information-room-name">房间名:{{ this.roomName }}</label>
            <br>
            <label id="information-teacher-name">主讲教师:{{ this.teacherName }}</label>
            <label class="person">
                <Icon type="person"></Icon>{{ this.studentNum }}
            </label>
        </a>
    </div>
</template>

<script>
import myMsg from './../warning.js'
export default {
    name: 'live-picture',
    props: ['roomName', 'teacherName', 'studentNum', 'id'],
    components: {
    },
    data: function () {
        return {
            stuAccount: '',
            joinOrNot: false
        }
    },
    created: function () {
        let arrCookies = document.cookie.split(';')
        for (let i = 0; i < arrCookies.length; i++) {
            let arrStr = arrCookies[i].split('=')
            if (arrStr[0].replace(/(^\s*)|(\s*$)/g, '') === 'userAccount') {
                this.stuAccount = arrStr[1].replace(/(^\s*)|(\s*$)/g, '')
                break
            } else {
                this.stuAccount = ''
            }
        }
    },
    methods: {
        liveRoom: function () {
            // 如果用户已经登录
            if (this.stuAccount) {
                fetch('/joinRoom/', {
                    method: 'post',
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json, text/plain, */*',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        'roomID': this.id,
                        'stuAccount': this.stuAccount
                    })
                }).then((response) => response.json()).then((obj) => {
                    if (obj.result === 'cannot') {
                        this.$Message.error(myMsg.room['cannotJoin'])
                    } else {
                        window.open('./#/live_room/' + this.id)
                    }
                })
            } else {
                this.$Message.error(myMsg.account['loginNeeded'])
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

.person {
    float: right;
    padding-right: 10px;
}

.picture a {
    color: #464c5b;
}

.picture:hover {
    color: #22313F;
}
</style>