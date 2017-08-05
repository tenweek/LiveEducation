<template>
    <div class="mydiv">
        <a href="#" @click="record_room">
            <!--视频封面-->
            <span class="imgbox">
                <img src="../assets/001.jpg" alt="" />
            </span>
            <div class="item-font">
                <!--房间名称-->
                <h3 class="ellipsis">花吃了那鱼尾</h3>
                <!--id-->
                <span class="ellipsis">10001房</span>
                <!--昵称-->
                <p>
                    <span class="zb-name ellipsis fl">FarmerIslander</span>
                </p>
            </div>
        </a>
    </div>
</template>

<script>
export default {
    name: 'RecordPicture',
    components: {},
    data: function () {
        return {
        }
    },
    methods: {
        record_room: function () {
            window.open('./#/record_room/')
        }
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.mydiv {
    width: 290px;
    height: auto;
    z-index: 0;
}

.mydiv a {
    width: 100%;
    height: 100%;
    display: block;
    background: #f5f5f5;
    margin-right: 10px;
    -webkit-transition: all .3s linear;
    -moz-transition: all .3s linear;
    -o-transition: all .3s linear;
    transition: all .3s linear;
    box-sizing: border-box;
    border-bottom: 3px solid #f5f5f5;
}

.mydiv a:hover {
    border-bottom: 3px solid #ff6300;
}

.imgbox {
    width: 100%;
    overflow: hidden;
}

.imgbox img {
    display: block;
    max-width: 100%;
    margin: 0 auto;
}

h3 {
    width: 70%;
    font-size: 14px;
    color: #313131;
    position: relative;
    right: 50px;
}

.ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    word-wrap: normal;
    word-break: keep-all;
}

.item-font>span {
    display: block;
    width: 60px;
    font-size: 12px;
    text-align: right;
    color: red;
    position: absolute;
    right: 7px;
    top: 30px;
}

p {
    height: 20px;
    padding-top: 5px;
    overflow: hidden;
}

.zb-name {
    display: block;
    max-width: 180px;
    padding-left: 25px;
    line-height: 20px;
    font-size: 12px;
    color: #797979;
    background-image: url("../assets/user.png");
    background-repeat: no-repeat;
    background-position: center left;
    background-size: contain;
}

.item-font {
    background: #f5f5f5;
    padding: 5px 5px 3px;
    line-height: 20px;
    font-size: 12px;
    height: 48px;
    overflow: hidden;
    position: relative;
}

.fl {
    float: left
}
</style>