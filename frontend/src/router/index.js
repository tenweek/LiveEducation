import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import SignUp from '@/components/SignUp'

Vue.use(Router)

export default new Router({
  routes: [
    {
        path: '/',
        name: 'Hello',
        component: Hello
    },
    {
        path: '/signin',
        name: 'SignIn',
        component: SignUp
    }
  ]
})
