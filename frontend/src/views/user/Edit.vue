<script setup>
import { ref, watchEffect, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import request from '@/utils/request.js'
import message from '@/utils/message.js'
import { regionData } from 'element-china-area-data'
const route = useRoute()
const router = useRouter()

const userId = ref(null)
const cityList = ref([])
const districtList = ref([])
const selectedProvince = ref('')
const selectedCity = ref('')
const selectedDistrict = ref('')
// 下拉显示控制
const showProvince = ref(false)
const showCity = ref(false)
const showDistrict = ref(false)

// 切换省份
const handleProvinceChange = (item) => {
  selectedProvince.value = item.value
  cityList.value = item.children || []
  selectedCity.value = ''
  districtList.value = []
  selectedDistrict.value = ''
  showProvince.value = false
}
// 切换城市
const handleCityChange = (item) => {
  selectedCity.value = item.value
  districtList.value = item.children || []
  selectedDistrict.value = ''
  showCity.value = false
}
// 切换区县
const handleDistrictChange = (item) => {
  selectedDistrict.value = item.value
  showDistrict.value = false
}

const form = ref({
  id: '',
  username: '',
  nickname: '',
  mobile: '',
  email: '',
  sex: 0,
  vip: false,
  add: '',
  detailAddr: ''
})

// 拼接省市区+详细地址，同步到form.add（和新增页完全一致）
watchEffect(() => {
  let addr = ''
  const p = regionData.find(x => x.value === selectedProvince.value)
  if (p) {
    addr += p.label
    const c = p.children.find(x => x.value === selectedCity.value)
    if (c) {
      addr += c.label
      const d = c.children.find(x => x.value === selectedDistrict.value)
      if (d) addr += d.label
    }
  }
  if (form.value.detailAddr) {
    addr += form.value.detailAddr
  }
  form.value.add = addr
})

// 【重点】地址拆分：后端返回完整地址字符串，解析出省市区、详细地址
function splitAddress(fullAddr) {
  if (!fullAddr) return
  // 遍历省份
  for (const p of regionData) {
    if (fullAddr.startsWith(p.label)) {
      selectedProvince.value = p.value
      const remain1 = fullAddr.replace(p.label, '')
      // 遍历城市
      for (const c of p.children) {
        if (remain1.startsWith(c.label)) {
          cityList.value = p.children
          selectedCity.value = c.value
          const remain2 = remain1.replace(c.label, '')
          // 遍历区县
          for (const d of c.children) {
            if (remain2.startsWith(d.label)) {
              districtList.value = c.children
              selectedDistrict.value = d.value
              // 剩下的作为详细地址
              form.value.detailAddr = remain2.replace(d.label, '')
              return
            }
          }
          // 有省市，无区县
          form.value.detailAddr = remain2
          return
        }
      }
      // 只有省份，无城市
      form.value.detailAddr = remain1
      return
    }
  }
  // 没有匹配到省市区，全部放到详细地址
  form.value.detailAddr = fullAddr
}

// 获取用户详情
const getUserDetail = async () => {
  try {
    const res = await request.get(`/user/edit/${userId.value}`)
    form.value = res.data[0]
    message.success(res.msg)
  } catch (err) {
    message.error('获取用户详情失败')
  }
}

// 提交编辑
const submitEdit = async () => {
  if (!form.value.username) {
    message.error('用户名不能为空')
    return
  }
  if (!form.value.nickname) {
    message.error('昵称不能为空')
    return
  }
  try {
    const res = await request.post(`/user/update/${userId.value}`, form.value)
    if (res.code === 200) {
      message.success(res.msg)
      router.push('/user')
    } else if (res.code === 400 || res.code === 404) {
      message.warning(res.msg)
    }
  } catch (err) {
    message.error('提交失败')
  }
}

const goBack = () => {
  router.push('/user')
}

// 重置表单
const resetForm = () => {
  form.value = {
    id: '',
    username: '',
    nickname: '',
    mobile: '',
    email: '',
    sex: 0,
    vip: false,
    add: '',
    detailAddr: ''
  }
  selectedProvince.value = ''
  selectedCity.value = ''
  selectedDistrict.value = ''
  cityList.value = []
  districtList.value = []
  showProvince.value = false
  showCity.value = false
  showDistrict.value = false
}

// 空白处关闭下拉
onMounted(() => {
  document.addEventListener('click', () => {
    showProvince.value = false
    showCity.value = false
    showDistrict.value = false
  })
  userId.value = route.query.id
  getUserDetail()
})
</script>

<template>
  <div class="user-edit-page">
    <div class="page-header">
      <h2>编辑用户</h2>
      <button class="back-btn" @click="goBack">返回列表</button>
    </div>
    <div class="form-card">
      <form @submit.prevent="submitEdit">
        <div class="form-item">
          <label class="form-label">用户名 <span class="red">*</span></label>
          <input class="form-input" v-model="form.username" placeholder="请输入用户名" />
        </div>
        <div class="form-item">
          <label class="form-label">昵称 <span class="red">*</span></label>
          <input class="form-input" v-model="form.nickname" placeholder="请输入昵称" />
        </div>
        <div class="form-item">
          <label class="form-label">手机号</label>
          <input class="form-input" v-model="form.mobile" placeholder="请输入手机号" />
        </div>
        <div class="form-item">
          <label class="form-label">邮箱</label>
          <input class="form-input" v-model="form.email" placeholder="请输入邮箱" />
        </div>
        <div class="form-item">
          <label class="form-label">性别</label>
          <select class="form-select" v-model="form.sex">
            <option :value="0">未知</option>
            <option :value="1">男</option>
            <option :value="2">女</option>
          </select>
        </div>
        <div class="form-item">
          <label class="form-label">地址</label>
          <div class="area-group">
            <!-- 省份下拉 -->
            <div class="custom-select" @click.stop="showProvince = !showProvince">
              <div class="select-input">
                {{ selectedProvince ? regionData.find(p=>p.value===selectedProvince)?.label : '选择省份' }}
              </div>
              <div v-if="showProvince" class="select-dropdown">
                <div class="option-item" v-for="p in regionData" :key="p.value" @click.stop="handleProvinceChange(p)">
                  {{ p.label }}
                </div>
              </div>
            </div>
            <!-- 城市下拉 -->
            <div class="custom-select" @click.stop="showCity = !showCity">
              <div class="select-input">
                {{ selectedCity ? cityList.find(c=>c.value===selectedCity)?.label : '选择城市' }}
              </div>
              <div v-if="showCity" class="select-dropdown">
                <div class="option-item" v-for="c in cityList" :key="c.value" @click.stop="handleCityChange(c)">
                  {{ c.label }}
                </div>
              </div>
            </div>
            <!-- 区县下拉 -->
            <div class="custom-select" @click.stop="showDistrict = !showDistrict">
              <div class="select-input">
                {{ selectedDistrict ? districtList.find(d=>d.value===selectedDistrict)?.label : '选择区县' }}
              </div>
              <div v-if="showDistrict" class="select-dropdown">
                <div class="option-item" v-for="d in districtList" :key="d.value" @click.stop="handleDistrictChange(d)">
                  {{ d.label }}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="form-item">
          <label class="form-label">详细地址</label>
          <input class="form-input" v-model="form.detailAddr" placeholder="请输入街道、门牌号等详细信息" />
        </div>

        <div class="form-btn-group">
          <button type="submit" class="submit-btn">保存提交</button>
          <button type="button" class="reset-form-btn" @click="resetForm">重置</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.user-edit-page {
  padding: 20px;
  background-color: #f0f2f5;
  min-height: 100%;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
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
.red{
  color:#f56c6c;
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
.area-group{
  display:flex;
  gap:8px;
  width:100%;
  box-sizing: border-box;
}
/* ========== 自定义下拉样式 和新增页面完全一样 ========== */
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
