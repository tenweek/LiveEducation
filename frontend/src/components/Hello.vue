<template>
    <div>
        <button @click="signUp">注册</button>
        <button @click="login">登录</button>
    </div>
</template>

<script>
import SignUp from './SignUp'
import LogIn from './Login'

export default {
    name: 'Hello',
    components: {
        SignUp,
        LogIn
    },
    data () {
        return {}
    },
    methods: {
        signUp () {
            this.$router.push({path: '/signup'})
        },
        login () {
            let name = document.cookie.split(';')[0].split('=')[0]
            if (name !== '') {
                this.$Message.error('已经登录过了！')
            } else {
                this.$router.push({path: '/login'})
            }
        }
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>