<template>
  <div>
    <test-get></test-get>
    <form>
      账号:
      <input type="text" id="account" v-model="account" @blur="checkMail" /> 密码:
      <input type="password" id="password" v-model="password" maxlength="16" @blur="checkStrength" />
      <input type="submit" value="Submit" @click="showdata" />
    </form>
  </div>
</template>

<script>
import TestGet from './test_get'
//import PostGet from './test_post'

export default {
  name: 'hello',
  components: {
    TestGet,
  },
  data() {
    return {
      account: '',
      password: '',
    }
  },
  methods: {
    checkMail() {
      // 判断是不是邮箱
      if (this.account === '') { return }
      let myreg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/;
      if (!myreg.test(this.account)) {
        alert('邮箱错了啊摔！')
        return
      }
    },

    checkStrength() {
      // 判断密码强度
      if (this.password === '') { return }
      let aLvTxt = ['', '低', '中', '高'];
      let lv = 0;
      if (this.password.length < 6) {
        alert('密码起码要是6位以上啊摔！')
        return
      }
      if (this.password.match(/[a-z]/g)) { lv++; }
      if (this.password.match(/[0-9]/g)) { lv++; }
      if (this.password.match(/(.[^a-z0-9])/g)) { lv++; }
      if (lv < 2) {
        alert('密码太弱了啊摔！')
        return
      }
    },

    showdata() {
      // 获取输入的账号密码
      fetch('Hello', {
        method: 'post',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json, text/plain, */*',
          'Accept': 'application/json'
        },
        // /发送json消息需要执行一个序列化操作，发送一个字典类型
        body: JSON.stringify({ 'account': this.account, 'password': this.password })
      }).then((response) => response.json()).then((obj) => {
        alert(obj.account + ' and ' + obj.password)
      })
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>