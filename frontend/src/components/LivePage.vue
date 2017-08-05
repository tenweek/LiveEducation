<template>
    <div class="head_bg">
    <div class="content">
        <div class="header">
            <!--logo位置-->
            <img class="fl" src="../assets/app_logo.jpg" alt=""/>

            <!--导航菜单-->
            <ul class="head_nav fl">
                <li><a href="#">首页</a></li>
                <li class="active"><a href="#">直播</a></li>
                <li><a href="#">录播</a></li>
            </ul>
            <!--其他功能-->

            <div class="head-oth fr">
                <div class="fl"><a href="#">登录</a></div>
                <div class="fl"><a href="#">注册</a></div>
                <div class="fl dropdown">
                    <a>个人信息</a>
                    <div class="icon"></div>
                </div>
                <div class="fl"><a href="#">创建</a></div>
                <!--个人信息点击菜单内容-->
                <div class="header_twoul">
                    <ul>
                        <li><a href="#">修改昵称</a></li>
                        <li><a href="#">修改密码</a></li>
                        <li><a href="#">注销</a></li>
                    </ul>
                </div>
            </div>
        </div>
    </div>


<!--页面头部end-->

<!--直播房间star-->
<div class="mt_20">

    <div class="content">
        <div class="house_both">
            <ul>
                <!--直播房间枚举-->
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
                <li>
                    <live-picture></live-picture>
                </li>
            </ul>
        </div>
    </div>
</div>
</div>
</template>

<script>
import LivePicture from './LivePicture'

export default {
    name: 'LivePage',
    components: {
        LivePicture
    },
    data() {
        return {
        }
    },
    methods: {
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

/*<!--直播房间star-->*/
.house_both{
    width: 100%;
    overflow: hidden;
    position: relative;
}
.house_both ul li{
    width: 25%;
    float: left;
    display: inline-block;
    margin-bottom: 20px;
}

/*全局定义*/
* {
    margin: 0;
    padding: 0;
}

body,html {
    font-family: 微软雅黑
}

section {
    width: 100%;
    height: auto;
}

li {
    list-style: none
}

a{
    text-decoration: none
}

.fl {
    float: left
}

.fr {
    float: right
}

.line {
    border-top: 1px solid #f5f5f5;
    border-bottom: 1px solid #f5f5f5
}

.mt_20 {
    margin-top: 20px; 
    margin-bottom: 20px; 
    position:relative;
}

.content{
    width: 1200px;
    height: 50px;
    margin: 0 auto;
}

.ellipsis{
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    word-wrap: normal;
    word-break: keep-all;
}

/*导航栏*/
.head_bg {
    background-color: #404052;
    height: 50px;
}

.header {
    width: 100%;
    height: 50px;
    background: #404052;
    box-sizing: border-box;
}

/*logo大小*/
.header img {
    display: block;
    width: 40px;
    height: 40px;
    margin-top: 5px;
}

/*<!--导航菜单-->*/
.header .head_nav {
    margin-left: 60px;
    height: 50px;
}

.header .head_nav li {
    float: left;
    font-size: 18px;
    line-height: 50px;
    width: 75px;
    height: 50px;
    margin: 0px 1px;
    text-align: center;
}

live-room {
    width:100%;

}

/*一级导航添加active*/
.header .head_nav li:hover a {
    background-color: white;
    color: #404052 !important;
}

.header .head_nav li.active {
    background-color: white;
    color: #404052 !important;
}

.header .head_nav li.active a {
    background-color: white;
    color: #404052 !important;
}

.header .head_nav li a {
    display: block;
    color: white;
}
/*<!--其他功能-->*/
.header .head-oth {
    height: 50px;
    position: relative;
}

.header .head-oth>div {
    width: 72px;
    margin-left: 20px;
    text-align: center;
    line-height: 50px;
    font-size: 16px;
    position: relative;
}

.header .head-oth>div a {
    display: block;
    color: white;
}

/*个人信息*/
.header .head-oth .icon {
    position: absolute;
    top: 5px;
    right:-37px;
     width: 30px;
    height: 24px;
    line-height: 36px;
    text-align: center;
    margin: 0 auto;
    display: block;
    color: #007aff;
    float: right;
    cursor: pointer;
    overflow: hidden;
    background-image: url(../assets/head_bottom.png);
    background-repeat: no-repeat;
    background-position: bottom left;
}

/*<!--个人信息点击菜单内容-->*/
 .header_twoul {
     position: absolute !important;
     width: 90px !important;
     top: 49px;
     left: 185px;
     background-color: #404052;
     display: none;
     z-index: 9999;
 }

.header_twoul ul li {
    width: 90px;
    height: 30px;
    line-height: 30px;
    font-size: 14px;
    text-align: center;
}

.header_twoul ul li a {
    color: white;
}

/*鼠标移入效果*/
.header_twoul ul li:hover {
    background-color: #c2c2c2;
}
</style>