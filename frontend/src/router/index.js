import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '@/components/HomePage'
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
            component: HomePage
        },
        {
            path: '/signup',
            component: SignUp
        },
        {
            path: '/login',
            component: Login
        },
        {
            path: '/reset',
            component: Reset
        },
        {
            path: '/live_room/:id',
            component: LiveRoom
        },
        {
            path: '/record_page',
            component: RecordPage
        },
        {
            path: '/record_room/:id',
            component: RecordRoom
        },
        {
            path: '/live_page',
            component: LivePage
        }
    ]
})
