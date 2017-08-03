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
