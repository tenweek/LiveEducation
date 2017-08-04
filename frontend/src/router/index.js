import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import SignUp from '@/components/SignUp'
import Login from '@/components/Login'
import Reset from '@/components/Reset'
import LiveRoom from '@/components/LiveRoom'
import RecordRoom from '@/components/RecordRoom'

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
        },
        {
            path: '/record_room',
            name: 'record_room',
            component: RecordRoom
        }
    ]
})
