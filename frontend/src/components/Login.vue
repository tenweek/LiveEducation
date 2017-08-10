<template>
    <div id="bg">
        <div class="log-in">
            <div>
                <h2 id="title">登录</h2>
                <router-link to="/reset" id="reset-link">忘记密码？</router-link>
            </div>
            <div id="content">
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
    </div>
</template>

<script>
export default {
    name: 'Login',
    components: {},
    data: function () {
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
        getResult: function () {
            // 获取输入的账号密码
            fetch('/login/', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                // 发送json消息需要执行一个序列化操作，发送一个字典类型
                body: JSON.stringify({
                    'account': this.formCustom.account,
                    'password': this.formCustom.password
                })
            }).then((response) => response.json()).then((obj) => {
                if (obj.result) {
                    this.$Message.success('登录成功！')
                    document.cookie = 'userAccount=' + this.formCustom.account
                    this.$router.push({ path: '/' })
                } else {
                    this.$Message.error('账号或密码不正确！')
                }
            })
        }
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#login-button {
    margin-top: 30px;
    margin-left: -40px;
    margin-bottom: -30px;
}

.log-in {
    background-color: white;
    margin: 180px auto;
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

#bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('./../assets/asteroids.jpg');
    background-repeat: repeat;
    z-index: -1;
    margin: auto;
}

#title {
    font-size: x-large;
    position: absolute;
    margin-left: 223px;
    margin-top: -20px;
}

#content {
    margin-left: -15px;
    margin-right: 15px;
    margin-top: 40px;
}

#reset-link {
    margin-right: -300px;
}
</style>
