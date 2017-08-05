<template>
    <div class="bg">
        <div class="sign-up">
            <div>
                <h2>注册</h2>
                <router-link to="/login" id="login-link">已有账号？</router-link>
            </div>
            <div class="form-panel">
                <div>
                    <Form ref="formCustom" :model="formCustom" :rules="ruleCustom" :label-width="70">
                        <Form-item label="邮箱" prop="mail">
                            <Input placeholder="请输入注册邮箱" v-model="formCustom.mail"></Input>
                        </Form-item>
                        <Form-item label="用户名" prop="username">
                            <Input placeholder="请输入用户名" v-model="formCustom.username"></Input>
                        </Form-item>
                        <Form-item label="密码" prop="passwd">
                            <Input type="password" v-model="formCustom.passwd" placeholder="请输入密码"></Input>
                        </Form-item>
                        <Form-item label="确认密码" prop="passwdCheck">
                            <Input type="password" v-model="formCustom.passwdCheck" placeholder="请再次输入密码"></Input>
                        </Form-item>
                        <Form-item label="验证码" prop="vertification">
                            <Row>
                                <Col span="17">
                                <Input v-model="formCustom.verification" placeholder="请输入验证码"></Input>
                                </Col>
                                <Col span="7">
                                <Button type="ghost" @click="getVerification">获取验证码</Button>
                                </Col>
                            </Row>
                        </Form-item>
                        <Form-item>
                            <Button type="primary" @click="signUp" id="signup-btn">确认注册</Button>
                        </Form-item>
                    </Form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'sign-up',
    data: function () {
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
            formCustom: {
                mail: '',
                mailChecked: '',
                username: '',
                passwd: '',
                passwdCheck: '',
                vertification: '',
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
        signUp: function () {
            if (this.formCustom.mailChecked !== this.formCustom.mail) {
                this.$Message.error('请不要修改注册邮箱！')
                return
            }
            if (this.formCustom.passwd === '') {
                this.$Message.error('请输入密码！')
                return
            }
            if (this.formCustom.passwd !== this.formCustom.passwdCheck) {
                this.$Message.error('两次输入密码不一致！')
                return
            }
            if (this.formCustom.username === '') {
                this.$Message.error('用户名不能为空')
                return
            }
            if (this.formCustom.verification === '') {
                this.$Message.error('请输入验证码！')
                return
            }
            if (this.formCustom.verification !== this.formCustom.loginKey) {
                this.$Message.error('输入的验证码有误！')
                return
            }
            this.$Message.success('注册成功!')
            fetch('SignUp', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    'mail': this.formCustom.mail,
                    'password': this.formCustom.passwd,
                    'username': this.formCustom.username
                })
            }).then((response) => response.json()).then((obj) => {
                this.$router.push({ path: '/login' })
            })
        },
        getVerification: function () {
            if (this.formCustom.mail === '') {
                this.$Message.error('请输入邮箱！')
                return
            }
            let reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/
            if (!this.formCustom.mail.match(reg)) {
                this.$Message.error('邮箱格式有问题！')
                return
            }
            fetch('getVerification', {
                method: 'post',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json, text/plain, */*',
                    'Accept': 'application/json'
                },
                // 发送json消息需要执行一个序列化操作，发送一个字典类型
                body: JSON.stringify({ 'mail': this.formCustom.mail })
            }).then((response) => response.json()).then((obj) => {
                if (obj.verification === 'exist') {
                    this.$Message.error('账号已存在')
                    return
                }
                this.formCustom.loginKey = obj.verification
                this.formCustom.mailChecked = this.formCustom.mail
                console.log(this.formCustom.loginKey)
            })
        }
    }
}
</script>

<style scoped>
h2 {
    font: 30px "microsoft yahei";
    color: #000000;
    height: 30px;
    position: absolute;
    margin-left: 223px;
    margin-top: -20px;
}

.sign-up {
    background-color: rgb(255, 255, 255);
    margin: 30px auto;
    width: 505px;
    border-radius: 10px;
    box-shadow: 0 0 25px rgba(0, 0, 0, .04);
    box-sizing: border-box;
    padding-top: 80px;
    padding-bottom: 60px;
}

.form-panel {
    margin-left: 12%;
    margin-right: 12%;
    margin-top: 40px;
}

.bg {
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

#signup-btn {
    margin-left: -66px;
    margin-top: 30px;
}

#login-link {
    margin-right: -300px;
}
</style>