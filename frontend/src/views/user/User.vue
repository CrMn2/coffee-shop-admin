<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import request from '@/utils/request.js'
import message from '@/utils/message.js'
import { useRouter } from 'vue-router'
const router = useRouter()
const userList = ref([])
// 搜索条件
const searchForm = ref({
  name: '', // 姓名/昵称
  area: '', // 地区/地址
  sex: ''   // 性别：空全部，0未知，1男，2女
})
// 分页配置
const pageNum = ref(1)
const pageSize = ref(5)
const fetchUserList = async () => {
  try {
    const res = await request.get('/user/list')
    userList.value = res.data
  } catch (error) {
    console.error('获取用户列表失败:', error)
  }
}
// 监听搜索条件变化，只要搜索内容修改，页码重置到第1页
watch(searchForm, () => {
  pageNum.value = 1
}, { deep: true })
// 新增用户点击事件
const handleAdd = () => {
  message.success('跳转到新增页面')
  router.push('/user/add')
}
// 编辑：根据id跳转编辑页面
const handleEdit = (row) => {
  // url传参，编辑页面 useRoute 获取 id
  router.push(`/user/edit?id=${row.id}`)
}
// 删除用户
const handleDelete = async (row) => {
  if (!confirm(`确定要删除【${row.nickname}】吗？`)) return
  try {
    const res = await request.post(`/user/delete/${row.id}`)
    if (res.code === 200) {
      message.success('删除成功')
      fetchUserList() // 删除成功重新拉取列表
    } else if (res.code === 400 || res.code === 404) {
      message.warning(res.msg)
    } else {
      message.error(res.msg)
    }
  } catch (err) {
    message.error('删除失败')
  }
}
// 筛选计算属性：先过滤，再分页
const filterUserList = computed(() => {
  const filterArr = userList.value.filter(item => {
    // 昵称模糊匹配
    const nameMatch = searchForm.value.name === '' || item.nickname.includes(searchForm.value.name)
    // 地址模糊匹配：处理item.add为null/undefined，并且搜索词、地址都去除首尾空格
    const areaMatch = searchForm.value.area === '' || (item.add || '').trim().includes(searchForm.value.area.trim())
    // 性别匹配，空字符串代表全部
    const sexMatch = searchForm.value.sex === '' || item.sex === Number(searchForm.value.sex)
    return nameMatch && areaMatch && sexMatch
  })
  return filterArr
})
// 分页后的数据，增加页码边界矫正
const pageList = computed(() => {
  // 如果当前页码大于总页数，自动修正页码
  if (totalPage.value > 0 && pageNum.value > totalPage.value) {
    pageNum.value = totalPage.value
  }
  const start = (pageNum.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filterUserList.value.slice(start, end)
})
// 总条数
const total = computed(() => filterUserList.value.length)
// 总页数
const totalPage = computed(() => Math.ceil(total.value / pageSize.value))
// 上一页
const prevPage = () => {
  if (pageNum.value > 1) pageNum.value--
}
// 下一页
const nextPage = () => {
  if (pageNum.value < totalPage.value) pageNum.value++
}
// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    name: '',
    area: '',
    sex: ''
  }
  pageNum.value = 1
}
onMounted(() => {
  fetchUserList()
})
</script>
<template>
  <div class="user-page">
    <div class="page-header">
      <h2>用户管理</h2>
      <!-- 新增按钮 -->
      <button class="add-btn" @click="handleAdd">+ 新增用户</button>
    </div>
    <!-- 搜索区域 -->
    <div class="search-card">
      <div class="search-wrap">
        <div class="search-item">
          <label>姓名：</label>
          <input v-model="searchForm.name" placeholder="请输入昵称搜索" />
        </div>
        <div class="search-item">
          <label>地区：</label>
          <input v-model="searchForm.area" placeholder="请输入地址搜索" />
        </div>
        <div class="search-item">
          <label>性别：</label>
          <select v-model="searchForm.sex" class="sex-select">
            <option value="">全部</option>
            <option value="0">未知</option>
            <option value="1">男</option>
            <option value="2">女</option>
          </select>
        </div>
        <button class="reset-btn" @click="resetSearch">重置</button>
      </div>
    </div>
   <div class="table-wrap">
    <table class="user-table" v-if="pageList.length > 0">
      <thead>
        <tr>
          <th>用户名</th>
          <th>昵称</th>
          <th>性别</th>
          <th>创建时间</th>
          <th>更新时间</th>
          <th>VIP</th>
          <th>地址</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <!-- 使用分页之后的列表 pageList -->
        <tr v-for="item in pageList" :key="item.id">
          <td>{{ item.username }}</td>
          <td>{{ item.nickname }}</td>
          <td>
            <span v-if="item.sex === 1">男</span>
            <span v-else-if="item.sex === 2">女</span>
            <span v-else>未知</span>
          </td>
          <td>{{ item.create_time }}</td>
          <td>{{ item.update_time }}</td>
          <td>
            <span class="vip-tag" :class="item.vip ? 'vip-yes' : 'vip-no'">
              {{ item.vip ? '是' : '否' }}
            </span>
          </td>
          <td>{{ item.add }}</td>
          <td class="action-col">
            <button class="edit-btn" @click="handleEdit(item)">编辑</button>
            <button class="del-btn" @click="handleDelete(item)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>
 <!-- 无数据提示 -->
 <div class="empty-tip" v-else>
   暂无数据
 </div>
 <!-- 分页组件 -->
 <div class="pagination" v-if="total > 0">
   <span class="total-text">共 {{ total }} 条数据</span>
   <button @click="prevPage" :disabled="pageNum === 1">上一页</button>
   <span class="page-info">第 {{ pageNum }} / {{ totalPage }} 页</span>
   <button @click="nextPage" :disabled="pageNum >= totalPage">下一页</button>
 </div>
  </div>
 </div>
</template>
<style scoped>
.empty-tip {
  text-align: center;
  padding: 40px 0;
  color: #666;
}
.user-page {
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
.add-btn {
  padding:8px 16px;
  border: none;
  background-color:#1890ff;
  color:#fff;
  border-radius:6px;
  cursor:pointer;
  font-size:14px;
  transition: background-color 0.2s;
}
.add-btn:hover{
  background-color:#40a9ff;
}
/* 搜索卡片美化 */
.search-card {
  background: #ffffff;
  padding: 18px 22px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  margin-bottom: 18px;
}
.search-wrap {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}
.search-item {
  display: flex;
  align-items: center;
  gap: 8px;
}
.search-item label {
  color: #4b5563;
  white-space: nowrap;
  font-size: 15px;
}
.search-item input,
.sex-select {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  outline: none;
  font-size:14px;
  transition: all 0.2s;
  width: 160px;
}
.search-item input:focus,
.sex-select:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 3px rgba(24,144,255,0.1);
}
.reset-btn {
  padding: 8px 18px;
  border: none;
  background-color: #6b7280;
  color: #fff;
  border-radius: 6px;
  cursor: pointer;
  font-size:14px;
  transition: background-color 0.2s;
}
.reset-btn:hover {
  background-color: #4b5563;
}
.table-wrap {
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
  background: #fff;
}
.user-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
}
.user-table th {
  background-color: #1f2937;
  color: #fff;
  text-align: left;
  padding: 14px 14px;
  font-weight: 500;
  white-space: nowrap;
  font-size:14px;
}
.user-table td {
  padding: 14px 14px;
  border-bottom: 1px solid #f0f0f0;
  color: #4b5563;
  font-size:14px;
}
/* 鼠标悬浮高亮行 */
.user-table tbody tr:hover {
  background-color: #f8fafc;
}
.vip-tag {
  padding: 4px 10px;
  border-radius: 12px;
  font-size:13px;
}
.vip-yes {
  background: #e6f7ff;
  color: #1890ff;
}
.vip-no {
  background: #f2f2f2;
  color: #666;
}
/* 分页样式 */
.pagination {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap:12px;
  padding:16px 20px;
}
.pagination button{
  padding:6px 14px;
  border:1px solid #d1d5db;
  background:#fff;
  border-radius:6px;
  cursor:pointer;
  font-size:14px;
}
.pagination button:disabled{
  background:#f5f7fa;
  color:#aaa;
  cursor:not-allowed;
}
.page-info,.total-text{
  font-size:14px;
  color:#4b5563;
}
/* 操作列样式 */
.action-col{
  display:flex;
  gap:8px;
}
.edit-btn{
  padding:5px 10px;
  border:none;
  background:#1890ff;
  color:#fff;
  border-radius:4px;
  cursor:pointer;
  font-size:13px;
}
.edit-btn:hover{
  background:#40a9ff;
}
.del-btn{
  padding:5px 10px;
  border:none;
  background:#f56c6c;
  color:#fff;
  border-radius:4px;
  cursor:pointer;
  font-size:13px;
}
.del-btn:hover{
  background:#f78989;
}
</style>
