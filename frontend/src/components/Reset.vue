<template>
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
            <Button type="primary" @click="next">获取验证码</Button>
        </template>
        <template v-else-if="this.current === 1">
            <Form ref="formCustom" :model="formCustom" :rules="ruleCustom" :label-width="70">
                <Form-item label="验证码" prop="vertification">
                    <Input placeholder="请输入验证码" v-model="formCustom.vertification"></Input>
                </Form-item>
            </Form>
            <Button type="primary" @click="next">下一步</Button>
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
            <Button type="primary" @click="next">下一步</Button>
        </template>
        <template v-else>
            <p>修改密码成功！</p>
            <Button type="primary" @click="next">登录</Button>
            
        </template>
    </div>
</div>
</template>

<script>
    export default {
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
            current: 0,
            formCustom: {
                mail: '',
                passwd: '',
                passwdCheck: '',
                vertification: ''
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
            next () {
                if (this.current === 3) {
                    this.current = 0
                } else {
                    this.current += 1
                }
            }
        }
    }
</script>

<style scoped>
.reset {
    margin-top: 100px;
    margin-left: auto;
    margin-right: auto;
    padding: auto;
}

.step-bar {
    margin-top: 60px;
    width: 900px;
    margin-left: auto;
    margin-right: auto;
}

#current-step {
    margin-top: 60px;
    width: 505px;
    margin-left: auto;
    margin-right: auto;
}
</style>
