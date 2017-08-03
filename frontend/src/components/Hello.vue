<template>
    <div class="home-page">
        <div class="header">
            <home-page-header></home-page-header>
		</div>
        <div class="navigation">
            <div class="navigation-center">
                <a class="navigation-bar" href="#"><Icon type="home"></Icon> 首页</a> |               
                <a class="navigation-bar" href="#"><Icon type="university"></Icon> 直播</a> |               
                <a class="navigation-bar" href="#"><Icon type="videocamera"></Icon> 录播</a> |              
                <a class="navigation-bar" href="#" @click="create_room"><Icon type="ios-plus"></Icon> 创建房间</a>
            </div>
            <div class="navigation-right">
              	<a class="navigation-bar" href="#">登录</a> |
              	<a class="navigation-bar" href="#">注册</a> |
              	<Dropdown>
					<a href="javascript:void(0)">
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
        <div class="list">
			<div class="list-hint">
				<Icon type="university" class="icon-middle"></Icon>
                &nbsp;
				<label class="live-broadcast">正在直播</label>
                <label class="information">当前直播房间：</label>
                <a href="#" class="more"><b><label>查看更多 <Icon type="chevron-right"></Icon></label><b></a>
			</div>
			<div class="list-picture">
				<live-picture></live-picture>
			</div>
        </div>
        <div class="list">
			<div class="list-hint">
                <Icon type="videocamera" class="icon-middle"></Icon>
                &nbsp;
            	<label class="live-broadcast">录播课堂</label>
                <label class="information">共有录播视频：</label>
                <a href="#" class="more"><b><label>查看更多 <Icon type="chevron-right"></Icon></label><b></a>
			</div>
        </div>        
        <div class="footer">
            2017 &copy; 光宗耀组
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
        HomePageHeader,
    },
    data() {
        return {
        }
    },
    methods: {
        create_room(){
            this.$Modal.confirm({
                    render: (h) => {
                        return h('Input', {
                            props: {
                                value: this.value,
                                autofocus: true,
                                placeholder: 'Please enter the room name...'
                            },
                            on: {
                                input: (val) => {
                                    this.value = val;
                                }
                            }
                        })
                    }
                })
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .home-page{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
        position: relative;
        border-radius: 5px;
        overflow: hidden;
    }
    .header{
		height: 60px;
		width: 100%;
		font-size: 40px;
	}
    .navigation{
        background: #464c5b;
        padding: 8px 0;
        overflow: hidden;
        display: flex;
    }
    .navigation-center{
        margin: 0 auto;
        font-size:15px;
    }
    .navigation-right{
        float: right;
        margin-right: 15px;
		font-size:15px;
    }
    .navigation-bar:hover{
		color: gold;
	}
    .navigation a{
        color: #9ba7b5;
    }
    .list{
        height: 268px;
        background: #fff;
        box-shadow: 0 1px 1px rgba(0,0,0,.1);
        border: 1px solid #d7dde4;
        padding-left: 15px;
        padding-top: 4px;
        padding-right: 15px;
    }
	.list-picture{
        background: red;
	}
	.list-hint{
        height:30px;
        line-height:30px;
        width: 100%;
        font-size: 20px;
        display: flex;
        background: #efefef;
        border-radius: 15px;
        padding-left: 8px;
        padding-right: 20px;
	}
    .icon-middle{
        vertical-align: middle;
    }
    .information{
        margin: 0 auto;
        font-size: 15px;
    }
    .more{
        float: right;
        font-size: 15px;
    }	
    .layout-logo{
        width: 100px;
        height: 30px;
        background: #5b6270;
        border-radius: 5px;
        float: left;
        position: relative;
        top: 15px;
        left: 20px;
    }  
    .footer{
        background: #efefef;
        text-align: center;
        padding: 5px 0 5px;
        color: #9ea7b4;
    }
    .more{
        color: #464c5b;
    }

</style>