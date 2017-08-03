<template>
<div class="log-in">
    <div>
        <h2>登录</h2>
    </div>
    <div>
         <Form ref="formCustom" :model="formCustom" :rules="ruleCustom" :label-width="70">
            <Form-item label="账号" prop="account">
                <Input placeholder="请输入注册邮箱" v-model="formCustom.account"></Input>
            </Form-item>
            <Form-item label="密码" prop="password">
                <Input type="password" v-model="formCustom.password" placeholder="请输入密码"></Input>
            </Form-item>
            <Form-item>
                <Button id="login-button" type="primary" @click="getResult">登录</Button>
            </Form-item>
        </Form>

    </div>
</div>
</template>

<script>
export default {
    name: 'Login',
    components: {},
    data () {
        const validatePass = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入密码'))
            } else {
                callback()
            }
        }
        return {
            formCustom: {
                account: '',
                password: ''
            },
            ruleCustom: {
                account: [
                    { required: true, message: '邮箱不能为空', trigger: 'blur' },
                    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '密码不能为空', trigger: 'blur' },
                    { validator: validatePass, trigger: 'blur' }
                ]
            }
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
#login-button {
    margin-left: -66px;
}

.log-in {
    background-color: white;
    margin: 30px auto;
    width: 505px;
    border-radius: 10px;
    box-shadow: 0 0 25px rgba(0, 0, 0, .04);
    box-sizing: border-box;
    padding-top: 60px;
    padding-bottom: 60px;
}

Form {
    margin: 10px 12px;
}
</style>
