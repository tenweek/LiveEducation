<template>
    <div class="layout">
        <div class="title">
			mdzz——直播间
        </div>

        <div class="layout-ceiling">
            <div class="layout-ceiling-main">
              	<a class="navigation-bar" href="#">登录</a> |
              	<a class="navigation-bar" href="#">注册</a> |

              	<Dropdown>
					<a href="javascript:void(0)">
					个人信息
					<Icon type="arrow-down-b"></Icon>
					</a>
					<Dropdown-menu slot="list">
					<Dropdown-item>修改昵称</Dropdown-item>
					</Dropdown-menu>
				</Dropdown>

            </div>
        </div>
    
        <div class="layout-header">
			<div class="hint">
				<b><label class="cycle">· · · ·</label></b>
				<label class="live-broadcast">正在直播</label>
				<b><label class="cycle">· · · ·</label></b>
				<br>
			</div>

			<div class="picture">
				<live-picture></live-picture>
			</div>
	
			<div class="b"><a href="#"><label>...查看更多>></label></a></div>

        </div>

        <div class="layout-header">
			<div class="hint">
				<b><label class="cycle">· · · ·</label></b>
            	<label class="live-broadcast">录播列表</label>
            	<b><label class="cycle">· · · ·</label></b>
            	<br>
			</div>
        </div>
        
        <div class="layout-copy">
            2017 &copy; 光宗耀组
        </div>
    </div>
</template>

<script>
export default {
    name: 'live-room',
    components: {
    },
    data() {
        return {
        }
    },
    methods: {
        
    }
}

</script>

<style>
</style>