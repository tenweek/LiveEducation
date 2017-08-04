<<<<<<< HEAD
import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import LiveRoom from '@/components/LiveRoom'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Hello',
            component: Hello
        },
        {
            path: '/live_room',
            name: 'live_room',
            component: LiveRoom
        }
    ]
})
=======
import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import SignUp from '@/components/SignUp'
import Login from '@/components/Login'
import Reset from '@/components/Reset'
import LiveRoom from '@/components/LiveRoom'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Hello',
            component: Hello
        },
        {
            path: '/signup',
            name: 'SignUp',
            component: SignUp
        },
        {
            path: '/login',
            name: 'Login',
            component: Login
        },
        {
            path: '/reset',
            name: 'Reset',
            component: Reset
        },
        {
            path: '/live_room',
            name: 'live_room',
            component: LiveRoom
        }
    ]
})
>>>>>>> b11a7a4777db9e1358d1cdcab558f72bbaa96fde
