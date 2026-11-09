<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const goHome = () => {
  const token = localStorage.getItem('token')
  if (token) {
    // 有token，跳后台首页
    router.push('/')
  } else {
    // 无token，跳登录页/admin
    router.push('/admin')
  }
}
</script>

<template>
  <div class="notfound">
    <h1>404</h1>
    <p>页面不存在</p>
    <button @click="goHome">返回首页</button>
  </div>
</template>


<style scoped>
.notfound {
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #666;
}
h1 {
  font-size: 72px;
  margin:0;
  color:#999;
}
button {
  margin-top:20px;
  padding:8px 16px;
  background:#409eff;
  color:white;
  border:none;
  border-radius:4px;
  cursor:pointer;
}
</style>
