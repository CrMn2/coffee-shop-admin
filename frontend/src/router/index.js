import { createRouter, createWebHistory } from 'vue-router'
// 导入页面组件
import Home from '../views/Home.vue'
import User from '../views/user/User.vue'
import Juice from '../views/juice/Juice.vue'
import Orders from '../views/orders/Orders.vue'
import UserAdd from '../views/user/Add.vue'
import UserEdit from '../views/user/Edit.vue'
import JuiceEdit from '../views/juice/Edit.vue'
import JuiceAdd from '../views/juice/Add.vue'
// admin 登录页面
import Admin from '../views/admin/Admin.vue'
// 404页面
import NotFound from '../views/NotFound.vue'
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: '数据总览', requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: { title: '管理员登录' }
  },
  {
    path: '/user',
    name: 'User',
    component: User,
    meta: { title: '用户管理', requiresAuth: true },
  },
  {
    path: '/user/add',
    name: 'UserAdd',
    component: UserAdd,
    meta: { title: '新增用户', requiresAuth: true }
  },
  {
    path: '/user/edit',
    name: 'UserEdit',
    component: UserEdit,
    meta: { title: '编辑用户', requiresAuth: true }
  },
  {
    path: '/juice',
    name: 'Juice',
    component: Juice,
    meta: { title: '饮品管理', requiresAuth: true }
  },
  {
    path: '/juice/edit',
    name: 'JuiceEdit',
    component: JuiceEdit,
    meta: { title: '编辑饮品', requiresAuth: true }
  },
  {
    path: '/juice/add',
    name: 'JuiceAdd',
    component: JuiceAdd,
    meta: { title: '新增饮品', requiresAuth: true }
  },
  {
    path: '/orders',
    name: 'Orders',
    component: Orders,
    meta: { title: '订单管理', requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { title: '页面不存在' }
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})
// 全局路由守卫 Vue Router4 新版写法
router.beforeEach((to, from) => {
  document.title = to.meta.title || '后台管理系统'
  const token = localStorage.getItem('token')
  // 目标页面需要登录校验
  if (to.meta.requiresAuth) {
    if (!token) {
      // 没有token，跳转到登录页
      return '/admin'
    }
    try {
      // 解析JWT payload
      const payloadStr = atob(token.split('.')[1])
      const payload = JSON.parse(payloadStr)
      // 判断是否过期 exp单位是秒 *1000转毫秒
      const isExpired = Date.now() > payload.exp * 1000
      if (isExpired) {
        // token过期，删除本地token，跳转登录
        localStorage.removeItem('token')
        return '/admin'
      }
    } catch (err) {
      // token格式错误，直接清理，跳登录
      localStorage.removeItem('token')
      return '/admin'
    }
    // token有效，放行
    return true
  } else {
    // 访问登录页面
    if (to.path === '/admin') {
      if (token) {
        try {
          const payloadStr = atob(token.split('.')[1])
          const payload = JSON.parse(payloadStr)
          const isExpired = Date.now() > payload.exp * 1000
          // token没过期，才跳首页；过期的话留在登录页
          if (!isExpired) {
            return '/'
          }else{
            localStorage.removeItem('token')
          }
        } catch (err) {
          localStorage.removeItem('token')
        }
      }
    }
    // 不需要权限页面，放行
    return true
  }
})
export default router
