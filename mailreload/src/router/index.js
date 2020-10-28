import Vue from 'vue'
import Router from 'vue-router'
import home from '@/components/home'
import emailList from '@/components/emailList'
import addEmailBox from '@/components/addEmailBox'
import email from '@/components/email'

Vue.use(Router)

const routes = [
  {
    path: '/',
    name: 'home',
    component: home,
    redirect:'emailList/all',
    children: [
      {
        path: 'emailList/:num',
        name: 'emailList1',
        component: emailList
      },
      {
        path: 'emailList/',
        name: 'emailList2',
        component: emailList
      },
      {
        path: 'addEmailBox/',
        name: 'addEmailBox',
        component: addEmailBox
      },
      {
        path: 'email/:num',
        name: 'email',
        component: email
      }
    ]
  }
]
const router = new Router({
  routes: routes
})
router.beforeEach((to, from, next) => {
  if (window._hmt) {
    if (to.path) {
      window._hmt.push(['_trackPageview', '/#' + to.fullPath])
    }
  }
  next()
})

export default router
