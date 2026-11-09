<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import request from '@/utils/request'
import message from '@/utils/message'
import * as echarts from 'echarts'

const overviewData = ref({
  totalUser: 0,
  totalOrder: 0,
  timeData: []
})
const drinkPieData = ref([])

let barChart = null
let pieChart = null

// 初始化柱状图
const initBarChart = () => {
  const dom = document.getElementById('barChartBox')
  barChart = echarts.init(dom)
  const option = {
    title: { text: '分时段数据对比' },
    tooltip: { trigger: 'axis' },
    legend: { data: ['新增用户', '新增订单', '饮品销量'] },
    xAxis: {
      type: 'category',
      data: overviewData.value.timeData.map(item => item.label)
    },
    yAxis: { type: 'value' },
    series: [
      { name: '新增用户', type: 'bar', data: overviewData.value.timeData.map(i => i.newUser), itemStyle:{color:'#4096ff'} },
      { name: '新增订单', type: 'bar', data: overviewData.value.timeData.map(i => i.newOrder), itemStyle:{color:'#ff7d00'} },
      { name: '饮品销量', type: 'bar', data: overviewData.value.timeData.map(i => i.drinkSale), itemStyle:{color:'#00b42a'} }
    ]
  }
  barChart.setOption(option)
}

// 初始化饼图（饮品类型占比）
// 初始化饼图（饮品类型占比）
const initPieChart = () => {
  const dom = document.getElementById('pieChartBox')
  pieChart = echarts.init(dom)
  const option = {
    title: {
      text: '饮品类型销量占比',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      bottom: 5,
      left: 'center',
      type: 'scroll', // 图例过多支持滚动
      orient: 'horizontal'
    },
    color:[
      '#4267E8', // 拿铁系列
      '#B4D62C', // 果茶系列
      '#4A4A64', // 瑞幸特调
      '#FF8C42', // 气泡特调
      '#00A8D8', // 甜品小食
      '#FFCC00', // 浓醇巧克力
      '#FF5789', // 清爽纯茶
      '#7A57A5', // 冰沙系列
      '#36B390', // 厚奶甜品
      '#4568D9', // 特调茶饮
      '#A4C928'  // 经典美式
    ],
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: true, // 防止标签重叠自动隐藏
      itemStyle: {
        borderRadius: 6
      },
      label: {
        show: true,
        position: 'outside'
      },
      labelLine: {
        show: true
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      data: drinkPieData.value
    }]
  }
  pieChart.setOption(option)
}


// 窗口大小变化自适应
const resizeChart = () => {
  barChart?.resize()
  pieChart?.resize()
}

// 请求后端接口
const getDashboardData = async () => {
  const res = await request.get('/index')
  if(res.code === 200){
    overviewData.value = res.data.overview
    drinkPieData.value = res.data.drinkPie
    message.success(res.msg)
    // 拿到数据之后再渲染图表
    initBarChart()
    initPieChart()
  }
}

onMounted(async ()=>{
  await getDashboardData()
  window.addEventListener('resize', resizeChart)
})

onUnmounted(() => {
  window.removeEventListener('resize', resizeChart)
  barChart?.dispose()
  pieChart?.dispose()
})
</script>


<template>
  <div class="dashboard">
    <h2>数据总览</h2>
    <!-- 顶部大盘卡片 -->
    <div class="card-group">
      <div class="card top-card blue">
        <h3>用户总人数</h3>
        <p class="num">{{ overviewData.totalUser }}</p>
      </div>
      <div class="card top-card orange">
        <h3>订单总数</h3>
        <p class="num">{{ overviewData.totalOrder }}</p>
      </div>
    </div>

    <!-- 分时段新增统计（彩色卡片） -->
    <h3 class="sub-title">分时段新增统计</h3>
    <div class="time-card-group">
      <div class="time-card" v-for="item in overviewData.timeData" :key="item.label" :style="{backgroundColor: item.cardColor}">
        <div class="time-title">{{ item.label }}</div>
        <div class="time-item">新增用户：<span>{{ item.newUser }}</span></div>
        <div class="time-item">新增订单：<span>{{ item.newOrder }}</span></div>
        <div class="time-item">饮品销量：<span>{{ item.drinkSale }}</span></div>
      </div>
    </div>

    <!-- 图表区域，左右并排：柱状图 + 饼图 -->
    <div class="chart-row">
      <div class="chart-box">
        <div id="barChartBox" style="width:100%;height:360px;"></div>
      </div>
      <div class="chart-box">
        <div id="pieChartBox" style="width:100%;height:360px;"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card-group {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}
.top-card.blue {
  background-color: #e8f4ff;
}
.top-card.orange {
  background-color: #fff3e8;
}
.card {
  border: 1px solid #eee;
  padding: 24px 32px;
  border-radius: 10px;
  min-width: 200px;
}
.num {
  font-size: 34px;
  font-weight: bold;
  color: #222;
  margin: 10px 0 0;
}
.sub-title {
  margin: 28px 0 14px;
}
.time-card-group {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
.time-card {
  border: 1px solid #eee;
  border-radius: 10px;
  padding:20px;
  min-width:160px;
}
.time-title {
  font-weight:bold;
  font-size:17px;
  margin-bottom:14px;
  color:#222;
}
.time-item {
  font-size:15px;
  margin:8px 0;
  color:#444;
}
.time-item span {
  font-weight:bold;
  color:#000;
}
/* 图表容器 左右两栏 */
.chart-row {
  display: flex;
  gap: 20px;
  margin-top:30px;
}
.chart-box {
  flex: 1;
  border:1px solid #eee;
  border-radius:10px;
  padding:16px;
  background:#fff;
}
</style>
