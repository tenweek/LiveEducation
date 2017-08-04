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
                                <Input placeholder="请输入注册邮箱" v-model="formCustom.mail"></Input>
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
export default {
    data() {
        const validatePass = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入密码'))
            } else {
                if (this.formCustom.passwdCheck !== '') {
                    // 对第二个密码框单独验证
                    this.$refs.formCustom.validateField('passwdCheck')
                }
                callback()
            }
        }
        const validatePassCheck = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请再次输入密码'))
            } else if (value !== this.formCustom.passwd) {
                callback(new Error('两次输入密码不一致!'))
            } else {
                callback()

            }
        }
        return {
            current: 0,
            formCustom: {
                mail: '',
                passwd: '',
                passwdCheck: '',
                verification: '',
                loginKey: ''
            },
            ruleCustom: {
                mail: [
                    { required: true, message: '邮箱不能为空', trigger: 'blur' },
                    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
                ],
                passwd: [
                    { required: true, message: '密码不能为空', trigger: 'blur' },
                    { validator: validatePass, trigger: 'blur' }
                ],
                passwdCheck: [
                    { required: true, message: '密码不能为空', trigger: 'blur' },
                    { validator: validatePassCheck, trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
        next() {
            this.current = 0
            this.$router.push({ path: '/login' })
        },
        getVerification() {
            fetch('getRand', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                // 发送json消息需要执行一个序列化操作，发送一个字典类型
                body: JSON.stringify({ 'mail': this.formCustom.mail })
            }).then((response) => response.json()).then((obj) => {
                if (obj.verification === 'none') {
                    this.$Message.error('用户不存在！')
                } else {
                    this.current += 1
                    this.formCustom.loginKey = obj.verification
                    console.log(this.formCustom.loginKey)
                }
            })
        },
        checkKey() {
            if (this.formCustom.verification !== this.formCustom.loginKey) {
                this.$Message.error('验证码错误！')
            } else {
                this.current += 1
            }
        },
        changePasswd() {
            if (this.formCustom.passwd !== this.formCustom.passwdCheck) {
                this.$Message.error('两次输入的密码不一致！')
            } else {
                fetch('changePasswd', {
                    method: 'post',
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json, text/plain, */*',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({
                        'username': this.formCustom.mail,
                        'password': this.formCustom.passwd
                    })
                }).then((response) => response.json()).then((obj) => {
                    this.current += 1
                })
            }
        }
    }
}
</script>

<style scoped>
.reset {
    margin-top: 80px;
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
    width: 90%  ;
    margin-left: 15px;
    padding-bottom: 30px;
}

#card {
    margin: 200px auto;
    width: 550px;
    margin-left: auto;
    margin-right: auto;
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