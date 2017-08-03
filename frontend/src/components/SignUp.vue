<template>
    <div class="background">
        <div class="sign-up">
            <div>
                <h2>注册</h2>
            </div>
            <div class="form-panel">
                <div>
                    <Form ref="formCustom" :model="formCustom" :rules="ruleCustom" :label-width="70">
                        <Form-item label="账号" prop="mail">
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
                            <Button type="primary" @click="signUp" id="midBtn">确认注册</Button>
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
    data () {
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
                loadRand: ''
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
        signUp () {
            if (this.formCustom.mailChecked !== this.formCustom.mail) {
                this.$Message.error('请不要修改注册邮箱！')
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
            if (this.formCustom.verification !== this.formCustom.loadRand) {
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
                this.$router.push({path: '/'})
            })
        },
        getVerification () {
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
                this.formCustom.loadRand = obj.verification
                this.formCustom.mailChecked = this.formCustom.mail
                console.log(this.formCustom.loadRand)
            })
        }
    }
}
</script>

<style scoped>
.sign-up {
    background-color: white;
    margin: 30px auto;
    width: 505px;
    border-radius: 10px;
    box-shadow: 0 0 25px rgba(0, 0, 0, .04);
    box-sizing: border-box;
    padding-top: 60px;
    padding-bottom: 60px;
}

.form-panel {
    margin: 10px 12%;
}

.background {
    background-color: rgb(230, 230, 230);
    margin: auto;
}

#midBtn {
    margin-left: -66px;
}
</style>