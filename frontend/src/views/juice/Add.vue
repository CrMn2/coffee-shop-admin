<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import request from '@/utils/request.js'
import message from '@/utils/message.js'
const router = useRouter()

// 下拉面板显示控制
const showCategory = ref(false)
// 表单数据
const form = ref({
  name: '',
  category: '',
  intro: '',
  price: '',
  vipPrice: '',
  isRecommend: 0
})
// 分类下拉选项
const categoryOptions = ref([])

// 获取分类列表（后端接口动态加载，替换静态数据）
const getCategoryList = async () => {
  const res = await request.get('/juice/category/list')
  if (res.code === 200) {
    categoryOptions.value = res.data
  }
}

// 选中已有类别
const handleCategorySelect = (item) => {
  form.value.category = item.name
  showCategory.value = false
}

// 提交
const onSubmit = async () => {
  // 前端表单校验
  if (!form.value.name) {
    message.warning('请输入饮品名称')
    return
  }
  if (!form.value.category) {
    message.warning('请选择或输入饮品类别')
    return
  }
  if (!form.value.intro) {
    message.warning('请输入饮品简介')
    return
  }
  if (!form.value.price || isNaN(form.value.price)) {
    message.warning('售价必须填写数字')
    return
  }
  if (!form.value.vipPrice || isNaN(form.value.vipPrice)) {
    message.warning('会员价必须填写数字')
    return
  }
  try {
    const res = await request.post('/juice/add', form.value)
    if (res.code === 200) {
      message.success('新增饮品成功')
      router.push('/juice')
    } else if (res.code === 400) {
      message.warning(res.msg)
    }
  } catch (err) {
    message.error('请求异常，新增失败')
    console.error(err)
  }
}

// 重置表单
const resetForm = () => {
  form.value = {
    name: '',
    category: '',
    intro: '',
    price: '',
    vipPrice: '',
    isRecommend: 0
  }
  showCategory.value = false
}

const goBack = () => {
  router.push('/juice')
}

// 点击空白关闭下拉
const closeDropdown = (e) => {
  showCategory.value = false
}

onMounted(() => {
  getCategoryList()
  document.addEventListener('click', closeDropdown)
})

// 组件销毁移除监听，防止内存泄漏
onUnmounted(() => {
  document.removeEventListener('click', closeDropdown)
})
</script>

<template>
  <div class="juice-add-page">
    <div class="page-header">
      <h2>新增饮品</h2>
      <button class="back-btn" @click="goBack">返回列表</button>
    </div>
    <div class="form-card">
      <form @submit.prevent="onSubmit">
        <div class="form-item">
          <label class="form-label">饮品名称</label>
          <input class="form-input" v-model="form.name" placeholder="请输入饮品名称" />
        </div>
        <div class="form-item">
          <label class="form-label">饮品类别</label>
          <div class="custom-select" @click.stop="showCategory = !showCategory">
            <div class="select-input">
              {{ form.category || '选择或输入饮品类别' }}
            </div>
            <div v-if="showCategory" class="select-dropdown">
              <div class="option-item" v-for="item in categoryOptions" :key="item.id" @click.stop="handleCategorySelect(item)">
                {{ item.name }}
              </div>
            </div>
            <!-- 手动输入框，支持新增类别 -->
            <input
              class="category-input"
              v-model="form.category"
              placeholder="输入新类别名称可新增"
              @click.stop
            />
          </div>
        </div>
        <div class="form-item">
          <label class="form-label">饮品简介</label>
          <textarea class="form-input textarea-input" v-model="form.intro" placeholder="请输入饮品简介"></textarea>
        </div>
        <div class="form-item">
          <label class="form-label">售价</label>
          <input class="form-input" type="number" step="0.01" min="0" v-model.number="form.price" placeholder="请输入售价" />
        </div>
        <div class="form-item">
          <label class="form-label">会员价</label>
          <input class="form-input" type="number" step="0.01" min="0" v-model.number="form.vipPrice" placeholder="请输入会员价" />
        </div>
        <div class="form-item">
          <label class="form-label">是否推荐</label>
          <select class="form-select" v-model="form.isRecommend">
            <option :value="0">不推荐</option>
            <option :value="1">推荐</option>
          </select>
        </div>
        <div class="form-btn-group">
          <button type="submit" class="submit-btn">提交保存</button>
          <button type="button" class="reset-form-btn" @click="resetForm">重置</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.juice-add-page {
  padding: 20px;
  background-color: #f0f2f5;
  min-height: 100%;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom:18px;
}
.page-header h2 {
  margin: 0;
  color: #1f2937;
  font-size: 24px;
  font-weight: 600;
}
.back-btn {
  padding: 8px 16px;
  border: none;
  background-color: #6b7280;
  color: #fff;
  border-radius: 6px;
  cursor: pointer;
  font-size:14px;
}
.back-btn:hover {
  background-color: #4b5563;
}
.form-card {
  background: #fff;
  padding: 24px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  max-width: 700px;
  overflow: visible;
}
.form-item {
  display: flex;
  align-items: center;
  margin-bottom:16px;
  box-sizing: border-box;
}
.form-label {
  width: 100px;
  flex-shrink:0;
  color:#4b5563;
  font-size:15px;
  line-height: 36px;
}
.form-input, .form-select {
  flex:1;
  box-sizing: border-box;
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius:6px;
  font-size:14px;
  height:36px;
}
.form-input:focus, .form-select:focus{
  outline:none;
  border-color:#1890ff;
  box-shadow:0 0 0 3px rgba(24,144,255,0.1);
}
.textarea-input {
  height: auto;
  min-height: 80px;
  resize: vertical;
}
/* ========== 自定义下拉 ========== */
.custom-select{
  flex:1;
  min-width:0;
  position:relative;
}
.select-input{
  height:36px;
  padding:0 12px;
  line-height:36px;
  border:1px solid #d1d5db;
  border-radius:6px;
  font-size:14px;
  background:#fff;
  cursor:pointer;
  white-space: nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}
.category-input{
  width: 100%;
  box-sizing: border-box;
  margin-top:6px;
  padding: 8px 12px;
  border:1px solid #d1d5db;
  border-radius:6px;
  font-size:14px;
  height:36px;
}
.select-dropdown{
  position:absolute;
  top:40px;
  left:0;
  right:0;
  max-height:220px;
  overflow-y:auto;
  background:#fff;
  border:1px solid #d1d5db;
  border-radius:6px;
  box-shadow:0 2px 8px rgba(0,0,0,0.08);
  z-index:10;
}
.option-item{
  padding:8px 12px;
  cursor:pointer;
  font-size:14px;
}
.option-item:hover{
  background:#e8f4ff;
}
.form-btn-group{
  margin-top:8px;
}
.submit-btn{
  padding:8px 20px;
  border: none;
  background-color:#1890ff;
  color:#fff;
  border-radius:6px;
  cursor:pointer;
  font-size:14px;
  margin-right:12px;
}
.submit-btn:hover{
  background-color:#40a9ff;
}
.reset-form-btn{
  padding:8px 20px;
  border:1px solid #d1d5db;
  background:#fff;
  color:#333;
  border-radius:6px;
  cursor:pointer;
  font-size:14px;
}
.reset-form-btn:hover{
  background:#f8fafc;
}
*{
    user-select: none;
}
</style>
