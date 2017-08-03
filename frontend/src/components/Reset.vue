<template>
<div class="reset">
    <div>
        <h2>重置密码</h2>
    </div>
    <div>
        <Steps :current="current">
            <Step title="填写资料"></Step>
            <Step title="验证身份"></Step>
            <Step title="设置新密码"></Step>
            <Step title="完成"></Step>
        </Steps>
    </div>
    <div id="current-step">
        <template v-if="this.current === 0">
            <Input v-model="email" placeholder="请输入注册邮箱" style="width: 300px"></Input>
            <Button type="primary" @click="next">获取验证码</Button>
        </template>
        <template v-else-if="this.current === 1">
            <Input v-model="vertification" placeholder="请输入验证码" style="width: 300px"></Input>
            <Button type="primary" @click="next">下一步</Button>
        </template>
        <template v-else-if="this.current === 2">
            
            <Input v-model="password" placeholder="请输入新密码" style="width: 300px"></Input>
            <br>
            <Input v-model="passwordcheck" placeholder="请再次输入新密码" style="width: 300px"></Input>
            <br>
            <Button type="primary" @click="next">下一步</Button>
        </template>
        <template v-else>
            <p>修改密码成功！</p>
            <Button type="primary" @click="next">登录</Button>
            
        </template>
    </div>
</div>
</template>

<script>
    export default {
        data () {
            return {
                current: 0
            }
        },
        methods: {
            next () {
                if (this.current == 3) {
                    this.current = 0;
                } else {
                    this.current += 1;
                }
            }
        }
    }
</script>

<style scoped>
.reset {
    margin-top: 160px;
    margin-left: auto;
    margin-right: auto;
    padding: auto;
}

#current-step {
    margin-top: 60px;
}
</style>
