<template>
<div class="background">
    <div class="sign-in">
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
	                        <Input v-model="formCustom.vertification" placeholder="请输入验证码"></Input>
	                    </Col>
	                    <Col span="7">
	                        <Button type="ghost">获取验证码</Button></Col></Row>
	                </Form-item>
	                <Form-item>
	                    
                        <Button type="primary" @click="handleSubmit('formCustom')">确认注册</Button>
                    </Form-item>
	            </Form>
	        </div>
	        
		</div>
	</div></div>
</template>

<script>
   export default {
        data () {
            const validatePass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入密码'));
                } else {
                    if (this.formCustom.passwdCheck !== '') {
                        // 对第二个密码框单独验证
                        this.$refs.formCustom.validateField('passwdCheck');
                    }
                    callback();
                }
            };
            const validatePassCheck = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请再次输入密码'));
                } else if (value !== this.formCustom.passwd) {
                    callback(new Error('两次输入密码不一致!'));
                } else {
                    callback();
                }
            };
            return {
                formCustom: {
                	mail: '',
                	username: '',
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
            handleSubmit (name) {
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        this.$Message.success('提交成功!');
                    } else {
                        this.$Message.error('表单验证失败!');
                    }
                })
            },
        }
    }
</script>

<style scoped>
.sign-in {
    background-color: white;
	margin: 30px auto;
	width: 39%;
	border-radius: 10px;
	box-shadow: 0 0 25px rgba(0,0,0,.04);
	box-sizing: border-box;
	padding-top: 60px;
	padding-bottom: 60px;
}
.form-panel{
	margin: 10px 12%;
}
.background {
	background-color: rgb(230,230,230);
	margin: auto;
}
</style>