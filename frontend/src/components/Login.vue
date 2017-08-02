<template>
    <form>
        账号:
        <input type="text" id="account" v-model="account" />
        <br> 密码:
        <input type="password" id="password" v-model="password" maxlength="16" />
        <br>
        <input type="submit" value="登录" @click="getResult" />
    </form>
</template>

<script>
export default {
    name: 'Login',
    components: {},
    data() {
        return {
            account: '',
            password: '',
        }
    },
    methods: {
        getResult() {
            // 获取输入的账号密码
            fetch('Login', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                // 发送json消息需要执行一个序列化操作，发送一个字典类型
                body: JSON.stringify({ 'account': this.account, 'password': this.password })
            }).then((response) => response.json()).then((obj) => {
                console.log(obj.result)
            })
        }
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>