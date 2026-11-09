<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import request from '@/utils/request.js'
import message from '@/utils/message.js'

const orderList = ref([])
// 搜索条件
const searchForm = ref({
  username: '', // 用户名称
  juiceName: '', // 饮品名称
})
// 分页配置
const pageNum = ref(1)
const pageSize = ref(5)

const fetchOrderList = async () => {
  try {
    const res = await request.get('/order/list')
    orderList.value = res.data
  } catch (error) {
    console.error('获取订单列表失败:', error)
  }
}

// 搜索变更重置页码
watch(searchForm, () => {
  pageNum.value = 1
}, { deep: true })

// 删除订单
const handleDelete = async (row) => {
  if (!confirm(`确定要删除这条订单【${row.id}】吗？`)) return
  try {
    const res = await request.post(`/order/delete/${row.id}`)
    if (res.code === 200) {
      message.success('删除成功')
      fetchOrderList()
    } else if (res.code === 400 || res.code === 404) {
      message.warning(res.message)
    } else {
      message.error(res.message)
    }
  } catch (err) {
    message.error('删除失败')
  }
}

// 筛选计算属性
const filterOrderList = computed(() => {
  const filterArr = orderList.value.filter(item => {
    const nameMatch = searchForm.value.username === '' || item.user.includes(searchForm.value.username)
    const juiceMatch = searchForm.value.juiceName === '' || item.juice.includes(searchForm.value.juiceName)
    return nameMatch && juiceMatch
  })
  return filterArr
})

// 分页数据
const pageList = computed(() => {
  if (totalPage.value > 0 && pageNum.value > totalPage.value) {
    pageNum.value = totalPage.value
  }
  const start = (pageNum.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filterOrderList.value.slice(start, end)
})

const total = computed(() => filterOrderList.value.length)
const totalPage = computed(() => Math.ceil(total.value / pageSize.value))

const prevPage = () => {
  if (pageNum.value > 1) pageNum.value--
}
const nextPage = () => {
  if (pageNum.value < totalPage.value) pageNum.value++
}

// 重置搜索
const resetSearch = () => {
  searchForm.value = {
    username: '',
    juiceName: ''
  }
  pageNum.value = 1
}

onMounted(() => {
  fetchOrderList()
})
</script>

<template>
  <div class="order-page">
    <div class="page-header">
      <h2>订单管理</h2>
      <!-- 没有新增按钮 -->
      <div></div>
    </div>
    <!-- 搜索区域 -->
    <div class="search-card">
      <div class="search-wrap">
        <div class="search-item">
          <label>用户：</label>
          <input v-model="searchForm.username" placeholder="请输入用户名搜索" />
        </div>
        <div class="search-item">
          <label>饮品：</label>
          <input v-model="searchForm.juiceName" placeholder="请输入饮品名称搜索" />
        </div>
        <button class="reset-btn" @click="resetSearch">重置</button>
      </div>
    </div>
    <div class="table-wrap">
      <table class="order-table" v-if="pageList.length > 0">
        <thead>
          <tr>
            <th>订单ID</th>
            <th>用户</th>
            <th>饮品</th>
            <th>数量</th>
            <th>订单金额</th>
            <th>收货地址</th>
            <th>下单时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in pageList" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.user }}</td>
            <td>{{ item.juice }}</td>
            <td>{{ item.juice_num }}</td>
            <td>{{ item.price }}</td>
            <td>{{ item.address }}</td>
            <td>{{ item.date }}</td>
            <td class="action-col">
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
.order-page {
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
.search-item input {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  outline: none;
  font-size:14px;
  transition: all 0.2s;
  width: 160px;
}
.search-item input:focus {
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
.order-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
}
.order-table th {
  background-color: #1f2937;
  color: #fff;
  text-align: left;
  padding: 14px 14px;
  font-weight: 500;
  white-space: nowrap;
  font-size:14px;
}
.order-table td {
  padding: 14px 14px;
  border-bottom: 1px solid #f0f0f0;
  color: #4b5563;
  font-size:14px;
}
.order-table tbody tr:hover {
  background-color: #f8fafc;
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
