<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from '@/utils/request.js'
import message from '@/utils/message.js'
const route = useRoute()
const router = useRouter()
const id = ref('')
const form = ref({
  type: '',
  title: '',
  content: '',
  price: '',
  vip_price: '',
  sales: '',
  is_recommend: ''
})

// 获取饮品详情
const getDetail = async () => {
  id.value = route.query.id
  try {
    const res = await request.get(`/juice/edit/${id.value}`)
    if(res.code === 200){
      form.value = res.data[0]
      message.success(res.msg)
    }else if(res.code === 400){
      message.warning(res.msg)
    }
  } catch (err) {
    message.error('加载详情失败')
  }
}

// 提交保存
const handleSubmit = async () => {
  try {
    const res = await request.post('/juice/update',{
      id: id.value,
      title: form.value.title,
      content: form.value.content,
      price: form.value.price,
      vip_price: form.value.vip_price,
      is_recommend: form.value.is_recommend
      // type、sales不提交，后端不修改
    })
    if(res.code === 200){
      message.success(res.msg)
      router.push('/juice') // 返回饮品列表
    }else{
      message.warning(res.msg)
    }
  } catch (err) {
    message.error('保存失败')
  }
}

// 返回
const goBack = () => {
  router.push('/juice')
}

onMounted(()=>{
  getDetail()
})
</script>

<template>
<div class="edit-page">
  <h2>编辑饮品</h2>
  <div class="form-card">
    <div class="form-item">
      <label>类别名称：</label>
      <input v-model="form.type" disabled placeholder="类别名称不可修改"/>
    </div>
    <div class="form-item">
      <label>饮品名称：</label>
      <input v-model="form.title" placeholder="请输入饮品名称"/>
    </div>
    <div class="form-item">
      <label>简介：</label>
      <textarea v-model="form.content" rows="3" placeholder="请输入饮品简介"></textarea>
    </div>
    <div class="form-item">
      <label>售价：</label>
      <input v-model="form.price" type="number" placeholder="请输入售价"/>
    </div>
    <div class="form-item">
      <label>会员价：</label>
      <input v-model="form.vip_price" type="number" placeholder="请输入会员价"/>
    </div>
    <div class="form-item">
      <label>销量：</label>
      <input v-model="form.sales" disabled placeholder="销量不可修改"/>
    </div>
    <div class="form-item">
      <label>是否推荐：</label>
      <select v-model="form.is_recommend">
        <option value="1">推荐</option>
        <option value="0">不推荐</option>
      </select>
    </div>
    <div class="btn-group">
      <button class="submit-btn" @click="handleSubmit">保存</button>
      <button class="back-btn" @click="goBack">返回</button>
    </div>
  </div>
</div>
</template>

<style scoped>
.edit-page{
  padding:20px;
  background-color:#f0f2f5;
  min-height:100%;
}
.edit-page h2{
  margin:0 0 18px 0;
  color:#1f2937;
}
.form-card{
  background:#fff;
  padding:24px;
  border-radius:10px;
  box-shadow:0 2px 10px rgba(0,0,0,0.06);
  max-width:600px;
}
.form-item{
  margin-bottom:16px;
  display:flex;
  flex-direction:column;
  gap:6px;
}
.form-item label{
  font-size:14px;
  color:#4b5563;
}
.form-item input,.form-item textarea,.form-item select{
  padding:10px;
  border:1px solid #d1d5db;
  border-radius:6px;
  font-size:14px;
}
.form-item input:disabled{
  background:#eee;
  color:#999;
  cursor:not-allowed;
}
.btn-group{
  display:flex;
  gap:12px;
  margin-top:20px;
}
.submit-btn{
  padding:8px 20px;
  background:#1890ff;
  color:#fff;
  border:none;
  border-radius:6px;
  cursor:pointer;
}
.back-btn{
  padding:8px 20px;
  background:#6b7280;
  color:#fff;
  border:none;
  border-radius:6px;
  cursor:pointer;
}
</style>
