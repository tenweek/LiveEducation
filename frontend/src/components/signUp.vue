<template>
    <form>
        账号:<input type="text" id="account" v-model="account" @blur="checkMail" /><br>
        密码:<input type="password" id="password" v-model="password" maxlength="16" @blur="checkStrength" /><br>
        <input type="submit" value="获取验证码" @click="getVerification" /><br>
        验证码：<input type="text" id="code" readonly><br>
        <input type="submit" value="注册" @click="signUp" />
    </form>
</template>

<script>
export default {
    name: 'signUp',
    components: {},
    data() {
        return {
            account: '',
            password: '',
            verification: '',
        }
    },
    methods: {
        signUp() {
            let code = document.getElementById('code').value
            if (code === this.verification) {
                alert('注册成功')
                fetch('login', {
                    method: 'post',
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json, text/plain, */*',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ 'account': this.account, 'password': this.password })
                }).then((response) => response.json()).then((obj) => {})
            } else {
                alert('照着输都能错？？？？？')
            }
        },

        checkMail() {
            // 判断邮箱是否符合标准
            if (this.account === '') { return }
            let myreg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/;
            if (!myreg.test(this.account)) {
                alert('输入的邮箱格式有问题')
                return
            }
        },

        checkStrength() {
            // 判断密码强度
            if (this.password === '') { return }
            let lv = 0;
            if (this.password.length < 6) {
                alert('密码长度应不短于6位！')
                return
            }
            if (this.password.match(/[a-z]/g)) { lv++; }
            if (this.password.match(/[0-9]/g)) { lv++; }
            if (this.password.match(/(.[^a-z0-9])/g)) { lv++; }
            if (lv < 2) {
                alert('密码强度过弱')
                return
            }
        },

        getVerification() {
            document.getElementById('code').readOnly = false;
            // 获取输入的账号密码
            fetch('Hello', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                // 发送json消息需要执行一个序列化操作，发送一个字典类型
                body: JSON.stringify({ 'account': this.account })
            }).then((response) => response.json()).then((obj) => {
                // 获取验证码
                this.verification = obj.verification
                console.log(this.verification)
            })
        }
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>