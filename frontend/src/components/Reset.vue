<template>
    <div id="bg">
        <Card id="card" shadow>
            <div class="reset">
                <div>
                    <h2>重置密码</h2>
                </div>
                <div class="step-bar">
                    <Steps :current="current">
                        <Step title="填写资料"></Step>
                        <Step title="验证身份"></Step>
                        <Step title="设置新密码"></Step>
                        <Step title="完成"></Step>
                    </Steps>
                </div>
                <div id="current-step">
                    <template v-if="this.current === 0">
                        <Form ref="formCustom" :model="formCustom" :rules="ruleCustom" :label-width="70">
                            <Form-item label="账号" prop="mail">
                                <Input placeholder="请输入注册邮箱或手机号" v-model="formCustom.mail"></Input>
                            </Form-item>
                        </Form>
                        <Button type="primary" id="nextBtn" @click="getVerification">获取验证码</Button>
                    </template>
                    <template v-else-if="this.current === 1">
                        <Form ref="formCustom" :model="formCustom" :rules="ruleCustom" :label-width="70">
                            <Form-item label="验证码" prop="vertification">
                                <Input placeholder="请输入验证码" v-model="formCustom.verification"></Input>
                            </Form-item>
                        </Form>
                        <Button type="primary" id="nextBtn" @click="checkKey">下一步</Button>
                    </template>
                    <template v-else-if="this.current === 2">
                        <Form ref="formCustom" :model="formCustom" :rules="ruleCustom" :label-width="70">
                            <Form-item label="密码" prop="passwd">
                                <Input type="password" v-model="formCustom.passwd" placeholder="请输入密码"></Input>
                            </Form-item>
                            <Form-item label="确认密码" prop="passwdCheck">
                                <Input type="password" v-model="formCustom.passwdCheck" placeholder="请再次输入密码"></Input>
                            </Form-item>
                        </Form>
                        <Button type="primary" id="nextBtn" @click="changePasswd">下一步</Button>
                    </template>
                    <template v-else>
                        <p>修改密码成功！</p>
                        <Button type="primary" id="nextBtn" @click="next">登录</Button>
                    </template>
                </div>
            </div>
        </Card>
    </div>
</template>

<script>
/**
 * 重置密码页
 *
 * @module Reset
 * @class Reset
 */
import myMsg from './../warning.js'
export default {
    data: function () {
        /**
         * 检验输入合法性
         *
         * @attribute validatePass
         * @readOnly
         * @type Object
         */
        const validatePass = (rule, value, callback) => {
            if (value === '') {
                callback(new Error(myMsg.account['passwordNeeded']))
            } else {
                if (this.formCustom.passwdCheck !== '') {
                    this.$refs.formCustom.validateField('passwdCheck')
                }
                callback()
            }
        }
        /**
         * 检验输入合法性
         *
         * @attribute validatePassCheck
         * @readOnly
         * @type Object
         */
        const validatePassCheck = (rule, value, callback) => {
            if (value === '') {
                callback(new Error(myMsg.account['passwordAgain']))
            } else if (value !== this.formCustom.passwd) {
                callback(new Error(myMsg.account['passwordAgainWrong']))
            } else {
                callback()
            }
        }
        return {
            /**
             * 表示当前正在执行的操作（进度条状态）
             *
             * @attribute current
             * @type Number
             * @default 0
             */
            current: 0,
            /**
             * 检验输入合法性
             *
             * @attribute formCustom
             * @type Object
             */
            formCustom: {
                mail: '',
                passwd: '',
                passwdCheck: '',
                verification: '',
                loginKey: ''
            },
            /**
             * 检验输入合法性
             *
             * @attribute ruleCustom
             * @type Object
             */
            ruleCustom: {
                mail: [
                    { required: true, message: myMsg.account['mailNeeded'], trigger: 'blur' }
                ],
                passwd: [
                    { required: true, message: myMsg.account['passwordNeeded'], trigger: 'blur' },
                    { validator: validatePass, trigger: 'blur' }
                ],
                passwdCheck: [
                    { required: true, message: myMsg.account['passwordNeeded'], trigger: 'blur' },
                    { validator: validatePassCheck, trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
        /**
         * 获取验证码，调用getMailVerification或getPhoneVerification函数
         *
         * @method getVerification
         */
        getVerification: function () {
            if (this.checkEmailAndPhone() === 0) {
                return
            } else if (this.checkEmailAndPhone() === 1) {
                this.getPhoneVerification()
            } else {
                this.getPhoneVerification()
            }
        },
        /**
         * 获取手机验证码
         *
         * @method getPhoneVerification
         */
        getPhoneVerification: function () {
            fetch('/getPhoneRand/', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'phoneNum': this.formCustom.mail
                })
            }).then((response) => response.json()).then((obj) => {
                if (obj.verification === 'none') {
                    this.$Message.error(myMsg.account['mailNotExist'])
                } else {
                    this.current = 1
                    this.formCustom.loginKey = obj.verification
                    console.log(this.formCustom.loginKey)
                }
            })
        },
        /**
         * 检查邮箱或手机号输入正确性
         *
         * @method checkEmailAndPhone
         */
        checkEmailAndPhone: function () {
            if (this.formCustom.mail === '') {
                this.$Message.error('请输入邮箱或手机号')
                return 0
            }
            let regMail = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/
            let regPhone = /^1(3|4|5|7|8)\d{9}$/
            if (this.formCustom.mail.match(regMail)) {
                return 1
            } else if (this.formCustom.mail.match(regPhone)) {
                return 2
            } else {
                this.$Message.error('请输入正确邮箱或手机号')
                return 0
            }
        },
        /**
         * 进度条进入下一个状态
         *
         * @method next
         */
        next: function () {
            this.current = 0
            this.$router.push({ path: '/login' })
        },
        /**
         * 获取邮箱验证码
         *
         * @method getVerification
         */
        getMailVerification: function () {
            fetch('/getMailRand/', {
                method: 'post',
                credentials: 'same-origin',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ 'mail': this.formCustom.mail })
            }).then((response) => response.json()).then((obj) => {
                if (obj.verification === 'none') {
                    this.$Message.error(myMsg.account['mailNotExist'])
                } else {
                    this.current = 1
                    this.formCustom.loginKey = obj.verification
                    console.log(this.formCustom.loginKey)
                }
            })
        },
        /**
         * 检验验证码有效性
         *
         * @method checkKey
         */
        checkKey: function () {
            if (this.formCustom.verification !== this.formCustom.loginKey) {
                this.$Message.error(myMsg.account['verificationWrong'])
            } else {
                this.current = 2
            }
        },
        /**
         * 修改密码
         *
         * @method changePasswd
         */
        changePasswd: function () {
            if (this.formCustom.passwd !== this.formCustom.passwdCheck) {
                this.$Message.error(myMsg.account['passwordAgainWrong'])
            } else {
                fetch('/changePasswd/', {
                    method: 'post',
                    mode: 'cors',
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json, text/plain, */*',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        'username': this.formCustom.mail,
                        'password': this.formCustom.passwd
                    })
                }).then((response) => response.json()).then((obj) => {
                    this.current = 3
                })
            }
        }
    }
}
</script>

<style scoped>
.reset {
    margin-top: 26px;
    margin-left: auto;
    margin-right: auto;
    padding: auto;
}

.step-bar {
    margin-top: 60px;
    width: 90%;
    margin-left: auto;
    margin-right: auto;
}

#current-step {
    margin-top: 60px;
    width: 90%;
    margin-left: 15px;
    padding-bottom: 30px;
}

#card {
    width: 550px;
    position: absolute;
    top: 50%;
    margin-top: -187px;
    left: 50%;
    margin-left: -275px;
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

#nextBtn {
    margin-top: 20px;
}
</style>
