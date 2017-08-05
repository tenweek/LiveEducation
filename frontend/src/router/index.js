import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import SignUp from '@/components/SignUp'
import Login from '@/components/Login'
import Reset from '@/components/Reset'
import LiveRoom from '@/components/LiveRoom'
import RecordPage from '@/components/RecordPage'
import RecordRoom from '@/components/RecordRoom'
import LivePage from '@/components/LivePage'

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
            path: '/record_page',
            name: 'record_page',
            component: RecordPage
        },
        {
            path: '/record_room',
            name: 'record_room',
            component: RecordRoom
        },
        {
            path: '/live_page',
            name: 'live_page',
            component: LivePage
        }
    ]
})
