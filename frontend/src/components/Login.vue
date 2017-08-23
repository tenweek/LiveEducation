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
            <div id="signup-link">
                <span>没有账号？马上</span>
                <router-link to="/signup">注册</router-link>
            </div>
        </div>
    </div>
</template>

<script>
/**
 * 登录页面
 *
 * @module Login
 * @class Login
 */
import myMsg from './../warning.js'
export default {
    name: 'Login',
    components: {},
    data: function () {
        /**
         * 检验输入合法性
         *
         * @attribute validatePass
         * @readOnly
         */
        const validatePass = (rule, value, callback) => {
            if (value === '') {
                callback(new Error(myMsg.account['passwordNeeded']))
            } else {
                callback()
            }
        }
        const validateAccount = (rule, value, callback) => {
            let regMail = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/
            let regPhone = /^1(3|4|5|7|8)\d{9}$/
            if (!value.match(regMail) && !value.match(regPhone)) {
                callback(new Error('请输入正确的账号'))
            } else {
                callback()
            }
        }
        return {
            /**
             * 检验输入合法性
             *
             * @attribute formCustom
             * @type Object
             */
            formCustom: {
                account: '',
                password: ''
            },
            /**
             * 检验输入合法性
             *
             * @attribute ruleCustom
             * @type Object
             */
            ruleCustom: {
                account: [
                    { required: true, message: myMsg.account['mailNeeded'], trigger: 'blur' },
                    { validator: validateAccount, trigger: 'blur' }
                ],
                password: [
                    { required: true, message: myMsg.account['passwordNeeded'], trigger: 'blur' },
                    { validator: validatePass, trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
        /**
         * 显示登录的结果
         *
         * @method getResult
         */
        getResult: function () {
            fetch('/login/', {
                method: 'post',
                mode: 'cors',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'account': this.formCustom.account,
                    'password': this.formCustom.password
                })
            }).then((response) => response.json()).then((obj) => {
                if (obj.result) {
                    this.$Message.success(myMsg.account['loginSuccess'])
                    this.$router.push({ path: '/' })
                } else {
                    this.$Message.error(myMsg.account['loginFailed'])
                }
            })
        }
    }
}

</script>

<style scoped>
#login-button {
    margin-top: 30px;
    margin-left: -40px;
    margin-bottom: -30px;
}

.log-in {
    background-color: white;
    top: 50%;
    margin-top: -179.5px;
    left: 50%;
    margin-left: -252.5px;
    position: absolute;
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
    margin-left: 228.5px;
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

#signup-link {
    margin-top: 49px;
    margin-bottom: -60px;
    border-bottom-left-radius: inherit;
    border-bottom-right-radius: inherit;
    background-color: #ffffd2;
    height: 45px;
    padding-top: 14px;
}
</style>
