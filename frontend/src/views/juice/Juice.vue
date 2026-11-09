<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import request from '@/utils/request.js'
import message from '@/utils/message.js'
import { useRouter } from 'vue-router'
const router = useRouter()
const juiceList = ref([])
// 搜索条件：类别名称、饮品名称、价格范围、销量范围、是否推荐
const searchForm = ref({
  type: '',
  title: '',
  priceMin: '',
  priceMax: '',
  salesMin: '',
  salesMax: '',
  is_recommend: ''
})
// 分页配置
const pageNum = ref(1)
const pageSize = ref(5)
const fetchJuiceList = async () => {
  try {
    const res = await request.get('/juice/list')
    juiceList.value = res.data
  } catch (error) {
    console.error('获取饮品列表失败:', error)
  }
}
// 前端过滤
const filterJuiceList = computed(() => {
  return juiceList.value.filter(item => {
    // 类别名称模糊匹配
    const typeMatch = searchForm.value.type === '' || item.type.includes(searchForm.value.type)
    // 饮品名称模糊匹配
    const titleMatch = searchForm.value.title === '' || item.title.includes(searchForm.value.title)
    // 价格范围判断
    let priceMatch = true
    if (searchForm.value.priceMin !== '') {
      priceMatch = priceMatch && item.price >= Number(searchForm.value.priceMin)
    }
    if (searchForm.value.priceMax !== '') {
      priceMatch = priceMatch && item.price <= Number(searchForm.value.priceMax)
    }
    // 销量范围判断
    let salesMatch = true
    if (searchForm.value.salesMin !== '') {
      salesMatch = salesMatch && item.sales >= Number(searchForm.value.salesMin)
    }
    if (searchForm.value.salesMax !== '') {
      salesMatch = salesMatch && item.sales <= Number(searchForm.value.salesMax)
    }
    // 是否推荐下拉
    const recMatch = searchForm.value.is_recommend === '' || item.is_recommend === Number(searchForm.value.is_recommend)
    return typeMatch && titleMatch && priceMatch && salesMatch && recMatch
  })
})
// 分页切片数据
const pageList = computed(() => {
  // 边界保护：页码不能超过总页数
  if (totalPage.value > 0 && pageNum.value > totalPage.value) {
    pageNum.value = totalPage.value
  }
  const start = (pageNum.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filterJuiceList.value.slice(start, end)
})
// 总条数、总页数
const total = computed(() => filterJuiceList.value.length)
const totalPage = computed(() => Math.ceil(total.value / pageSize.value))
// 分页方法
const prevPage = () => {
  if (pageNum.value > 1) pageNum.value--
}
const nextPage = () => {
  if (pageNum.value < totalPage.value) pageNum.value++
}
// 重置搜索，并且回到第一页
const resetSearch = () => {
  searchForm.value = {
    type: '',
    title: '',
    priceMin: '',
    priceMax: '',
    salesMin: '',
    salesMax: '',
    is_recommend: ''
  }
  pageNum.value = 1
}
// 监听搜索表单变化，自动回到第1页（解决页码错乱核心代码）
watch(searchForm, () => {
  pageNum.value = 1
}, { deep: true })

// 新增饮品
const handleAdd = () => {
  message.success('跳转到新增饮品页面')
  router.push('/juice/add')
}
// 编辑：路由跳转，url传id，编辑页面接收id
const handleEdit = (row) => {
  router.push(`/juice/edit?id=${row.id}`)
}
// 删除饮品
const handleDelete = async (row) => {
  if (!confirm(`确定要删除【${row.title}】吗？`)) return
  try {
    const res = await request.post(`/juice/delete/${row.id}`)
    if (res.code === 200) {
      message.success(res.msg)
      fetchJuiceList() // 删除成功刷新列表
    } else if (res.code === 400 || res.code === 404) {
      message.warning(res.msg)
    } else {
      message.error(res.msg)
    }
  } catch (err) {
    message.error('删除失败')
  }
}

onMounted(() => {
  fetchJuiceList()
})
</script>

<template>
  <div class="juice-page">
    <div class="page-header">
      <h2>饮品管理</h2>
      <!-- 新增按钮 -->
      <button class="add-btn" @click="handleAdd">+ 新增饮品</button>
    </div>
    <!-- 搜索卡片区域 -->
    <div class="search-card">
      <div class="search-wrap">
        <div class="search-item">
          <label>类别名称：</label>
          <input v-model="searchForm.type" placeholder="请输入类别名称" />
        </div>
        <div class="search-item">
          <label>饮品名称：</label>
          <input v-model="searchForm.title" placeholder="请输入饮品名称" />
        </div>
        <div class="search-item">
          <label>售价：</label>
          <input v-model="searchForm.priceMin" placeholder="最低" type="number" />
          <span class="range-line">~</span>
          <input v-model="searchForm.priceMax" placeholder="最高" type="number" />
        </div>
        <div class="search-item">
          <label>销量：</label>
          <input v-model="searchForm.salesMin" placeholder="最低" type="number" />
          <span class="range-line">~</span>
          <input v-model="searchForm.salesMax" placeholder="最高" type="number" />
        </div>
        <div class="search-item">
          <label>是否推荐：</label>
          <select v-model="searchForm.is_recommend" class="rec-select">
            <option value="">全部</option>
            <option value="1">推荐</option>
            <option value="0">不推荐</option>
          </select>
        </div>
        <button class="reset-btn" @click="resetSearch">重置</button>
      </div>
    </div>
    <div class="table-wrap">
      <!-- 有数据展示表格 -->
      <table class="juice-table" v-if="pageList.length > 0">
        <thead>
          <tr>
            <th>类别名称</th>
            <th>饮品名称</th>
            <th>简介</th>
            <th>售价</th>
            <th>会员价</th>
            <th>销量</th>
            <th>是否推荐</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <!-- ✅ 整行点击跳转编辑，加鼠标手型样式 -->
          <tr v-for="item in pageList" :key="item.id" @click="handleEdit(item)" class="row-clickable">
            <td>{{ item.type }}</td>
            <td>{{ item.title }}</td>
            <td>{{ item.content }}</td>
            <td>¥{{ item.price }}</td>
            <td>¥{{ item.vip_price }}</td>
            <td>{{ item.sales }}</td>
            <td>
              <span class="recommend-tag" :class="item.is_recommend ? 'rec-yes' : 'rec-no'">
                {{ item.is_recommend ? '推荐' : '不推荐' }}
              </span>
            </td>
            <td class="action-col" @click.stop>
              <!-- @click.stop：阻止点击删除按钮时触发行跳转 -->
              <button class="del-btn" @click="handleDelete(item)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
      <!-- 无数据提示，和用户管理样式统一 -->
      <div class="empty-tip" v-else>
        暂无数据
      </div>
      <!-- 分页栏：只有数据大于0的时候才显示分页 -->
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
.juice-page {
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
.rec-select {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  outline: none;
  font-size:14px;
  transition: all 0.2s;
  width: 120px;
}
.search-item input:focus,
.rec-select:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 3px rgba(24,144,255,0.1);
}
.range-line {
  color:#666;
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
.juice-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
}
.juice-table th {
  background-color: #1f2937;
  color: #fff;
  text-align: left;
  padding: 14px 14px;
  font-weight: 500;
  white-space: nowrap;
  font-size:14px;
}
.juice-table td {
  padding: 14px 14px;
  border-bottom: 1px solid #f0f0f0;
  color: #4b5563;
  font-size:14px;
}
.juice-table tbody tr:hover {
  background-color: #f8fafc;
}
.recommend-tag {
  padding: 4px 10px;
  border-radius: 12px;
  font-size:13px;
}
.rec-yes {
  background: #e6ffe6;
  color: #009944;
}
.rec-no {
  background: #f2f2f2;
  color: #666;
}
/* 分页样式，和用户管理页面保持一致 */
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
.row-clickable{
  cursor: pointer;
}
.row-clickable:hover {
  background-color: #eef6ff !important;
}

</style>
