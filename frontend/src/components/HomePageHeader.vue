<template>
    <div class="title">
        <div class="logo">
            <a href="#">
            <img src="../assets/rabbit.png" height="60">
            <label id="mdzz">MDZZ</label>
            </a>    
        </div>
        <div class="navigation-center">
            <a class="navigation-bar" href="#"><Icon type="home"></Icon> 首页</a> |               
            <a class="navigation-bar" href="#"><Icon type="university"></Icon> 直播</a> |               
            <a class="navigation-bar" href="#"><Icon type="videocamera"></Icon> 录播</a> |           
            <a class="navigation-bar" href="#" @click="modal1 = true"><Icon type="ios-plus"></Icon> 创建房间</a>
            <Modal
                v-model="modal1"
                title="创建房间"
                @on-ok="ok"
                @on-cancel="cancel">
                <label>房间名称：</label>
                <Input v-model="value1" size="large" placeholder="请输入房间名称"></Input><br><br>
                <p>上传课件</p>

                <Upload action="//jsonplaceholder.typicode.com/posts/">
                    <div class="upload">    
                        <Button type="ghost">点击选择文件&nbsp;&nbsp;
                        <Icon type="folder"></Icon>
                        </Button>
                    </div>                        
                </Upload><br>
                <p>上传封面图</p>
                <Upload action="//jsonplaceholder.typicode.com/posts/">
                    <div class="upload">    
                        <Button type="ghost">                                
                        点击选择图片&nbsp;&nbsp;<Icon type="image"></Icon>
                        </Button>
                    </div>
                </Upload>
            </Modal>            
        </div>

        <div class="navigation-right">
            <a class="navigation-bar" href="#/login">登录</a> |
            <a class="navigation-bar" href="#/signup">注册</a> |
            <Dropdown>
                <a class="navigation-bar" href="javascript:void(0)">
                个人信息
                <Icon type="arrow-down-b"></Icon>
                </a>
                <Dropdown-menu slot="list">
                <Dropdown-item>修改昵称</Dropdown-item>
                <Dropdown-item>修改密码</Dropdown-item>
                </Dropdown-menu>
            </Dropdown>
        </div>

    </div>
</template>

<script>
    export default {
    name: 'home-page-header',
    components: {
    },
    data () {
        return {
            modal1: false,
            value1: ''
        }
    },
    methods: {
        ok () {
             this.$Message.info('您已成功创建房间！')
        },
        cancel () {
            this.$Message.info('点击了取消')
        }
    }
}
</script>

<style scoped>
    .title{
        height: 60px;
        line-height:60px;
        width: 100%;
        padding-left: 30px;
        background: white;
        position: fixed;
        background: #22313F;
        overflow: hidden;
        min-width: 1300px;
        display: flex;
    }
    .logo{
        width: 180px;
        height: 100%;
    }
    #mdzz{
        color: #ECFFFB;
        vertical-align: top;
        font-family: "Comic Sans MS";
        font-size: 35px;
    }
    .navigation-center{
        font-size:20px;
        padding-top: 14px;
        color: #9ba7b5;
        margin-left: 20px;
    }
    .navigation-right{
        float: right;
        margin-right: 15px;
        font-size:20px;
        padding-top: 14px;
        position: relative;
        margin-left: 40%;
    }
    .navigation-center a{
        color: #E4F1FE;
    }
    .navigation-right a{
        color: #E4F1FE;
    }
    .navigation-bar:hover{
        color: #FCE38A;
    }
</style>
