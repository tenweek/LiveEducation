<<<<<<< HEAD
<template>
  <div>
    <test-get></test-get>
    <make-room></make-room>
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
import MakeRoom from './make_room'
// import PostGet from './test_post'

export default {
  name: 'hello',
  components: {
    TestGet,
    MakeRoom
  },
  data () {
    return {
      account: '',
      password: ''
    }
  },
  methods: {
    checkMail () {
      // 判断是不是邮箱
      if (this.account === '') { return }
      let myreg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/
      if (!myreg.test(this.account)) {
        alert('邮箱错了啊摔！')
        return
      }
    },

    checkStrength () {
      // 判断密码强度
      if (this.password === '') { return }
      // let aLvTxt = ['', '低', '中', '高']
      let lv = 0
      if (this.password.length < 6) {
        alert('密码起码要是6位以上啊摔！')
        return
      }
      if (this.password.match(/[a-z]/g)) { lv++ }
      if (this.password.match(/[0-9]/g)) { lv++ }
      if (this.password.match(/(.[^a-z0-9])/g)) { lv++ }
      if (lv < 2) {
        alert('密码太弱了啊摔！')
        return
      }
    },

    showdata () {
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

=======
<template>
    <div class="home-page">
        <div class="header">
            <home-page-header></home-page-header>
        </div>
        <div class="list">
            <div class="list-hint">
                <div class="icon">
                    <Icon type="university" class="icon-middle"></Icon>
                </div>
                &nbsp;
                <label class="live-broadcast">正在直播</label>
                <a href="#" class="more">
                    <b>
                        <label>查看更多
                            <Icon type="chevron-right"></Icon>
                        </label>
                    </b>
                </a>
            </div>
            <div class="list-picture">
                <live-picture></live-picture>
            </div>
        </div>
        <div class="list">
            <div class="list-hint">
                <div class="icon">
                    <Icon type="videocamera" class="icon-middle"></Icon>
                </div>
                &nbsp;
                <label class="live-broadcast">录播课堂</label>
                <a href="#" class="more">
                    <b>
                        <label>查看更多
                            <Icon type="chevron-right"></Icon>
                        </label>
                    </b>
                </a>
            </div>
        </div>
        <div class="footer">
            2017 &copy; 光宗耀组
        </div>
    </div>
</template>

<script>
import LivePicture from './LivePicture'
import HomePageHeader from './HomePageHeader'

export default {
    name: 'hello',
    components: {
        LivePicture,
        HomePageHeader
    },
    data: function () {
        return {}
    },
    methods: {}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.home-page {
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 5px;
    overflow: hidden;
}

.header {
    height: 60px;
    width: 100%;
    font-size: 40px;
}

.navigation {
    background: #464c5b;
    padding: 8px 0;
    overflow: hidden;
    display: flex;
}

.navigation-center {
    margin: 0 auto;
    font-size: 15px;
}

.navigation-right {
    float: right;
    margin-right: 15px;
    font-size: 15px;
}

.navigation-bar:hover {
    color: gold;
}

.navigation a {
    color: #9ba7b5;
}

.list {
    height: 295px;
    width: 1100px;
    background: #fff;
    box-shadow: 0 1px 1px rgba(0, 0, 0, .1);
    margin-left: 150px;
    margin-right: 150px;
    overflow: hidden;
    background: white;
    padding-top: 8px;
}

.list-picture {
    height: 100%;
    padding-top: 5px;
}

.list-hint {
    height: 45px;
    line-height: 45px;
    width: 100%;
    font-size: 25px;
    display: flex;
    padding-left: 20px;
    padding-right: 20px;
    border-bottom: solid;
}

.more {
    float: right;
    font-size: 15px;
    color: #464c5b;
    padding-top: 4px;
    margin-left: 850px;
}

.layout-logo {
    width: 100px;
    height: 30px;
    background: #5b6270;
    border-radius: 5px;
    float: left;
    position: relative;
    top: 15px;
    left: 20px;
}

.footer {
    text-align: center;
    padding: 5px 0 5px;
    color: #9ea7b4;
}
>>>>>>> b11a7a4777db9e1358d1cdcab558f72bbaa96fde
</style>