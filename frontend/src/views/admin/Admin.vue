<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import message from '@/utils/message.js'
import request from '@/utils/request.js'

const router = useRouter()
const loading = ref(false)
const form = ref({
  username: '',
  password: ''
})

// 登录逻辑
const handleLogin = async () => {
  loading.value = true
  try{
    const res = await request.post('/admin', form.value)
    if (res.code === 200){
      localStorage.setItem('token', res.data.token)
      message.success(res.msg)
      router.push('/')
    } else if (res.code === 401){
      message.error(res.msg)
    } else if (res.code === 400){
      message.warning(res.msg)
    }
  }finally {
    loading.value = false
  }
}




// 回车触发登录
const handleKeyEnter = (e) => {
  if (e.key === 'Enter') {
    handleLogin()
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-box">
      <h2>管理员登录</h2>
      <div class="form-item">
        <label>账号</label>
        <input 
          v-model="form.username" 
          type="text" 
          placeholder="请输入账号"
          @keyup="handleKeyEnter"
        />
      </div>
      <div class="form-item">
        <label>密码</label>
        <input 
          v-model="form.password" 
          type="password" 
          placeholder="请输入密码"
          @keyup="handleKeyEnter"
        />
      </div>
      <button 
        class="login-btn" 
        @click="handleLogin"
        :disabled="loading"
      >
        {{ loading ? '登录中...' : '登录' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  width: 100%;
  height: 100vh;
  background-color: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.login-box {
  width: 360px;
  padding: 32px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.08);
}
h2 {
  text-align: center;
  margin: 0 0 28px;
  color: #303133;
  font-size: 24px;
}
.form-item {
  margin-bottom: 20px;
}
label {
  display: block;
  margin-bottom: 8px;
  color: #606266;
  font-size: 14px;
}
input {
  width: 100%;
  box-sizing: border-box;
  padding: 11px 14px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}
input:focus {
  border-color: #409eff;
}
.login-btn {
  width: 100%;
  padding: 11px;
  background-color: #409eff;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 15px;
  transition: background 0.2s;
}
.login-btn:hover:not(:disabled) {
  background-color: #66b1ff;
}
.login-btn:disabled {
  background-color: #90cfff;
  cursor: not-allowed;
}
</style>
