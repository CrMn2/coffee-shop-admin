<script setup>
</script>
<template>
  <div v-if="$route.name !== 'NotFound' && $route.path !== '/admin'" class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-title">饮品后台管理系统</div>
      <nav class="nav-list">
        <router-link to="/" class="nav-item">
          <span class="nav-text">数据总览</span>
        </router-link>
        <router-link to="/user" class="nav-item">
          <span class="nav-text">用户管理</span>
        </router-link>
        <router-link to="/juice" class="nav-item">
          <span class="nav-text">饮品管理</span>
        </router-link>
        <router-link to="/orders" class="nav-item">
          <span class="nav-text">订单管理</span>
        </router-link>
      </nav>
    </aside>
    <main class="content">
      <router-view />
    </main>
  </div>
  <router-view v-else />
</template>

<style>
/* 全局重置，必须加 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
html,
body {
  height: 100%;
  /* 禁用浏览器外层滚动 */
  overflow: hidden;
}
#app {
  height: 100%;
}
</style>

<style scoped>
.admin-layout {
  display: flex;
  /* ✅ 换成100%，不要100vh，100vh容易出现滚动bug */
  height: 100%;
  overflow: hidden;
}
.sidebar {
  width: 220px;
  background: #2c3e50;
  display: flex;
  flex-direction: column;
}
.sidebar-title {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid #34495e;
}
.nav-list {
  padding-top: 20px;
}
.nav-item {
  display: block;
  color: #cbd5e0;
  padding: 14px 24px;
  text-decoration: none;
  transition: all 0.25s;
  border-left: 3px solid transparent;
}
.nav-item:hover {
  background-color: #34495e;
  color: #ffffff;
}
.nav-item.router-link-active {
  background-color: #34495e;
  color: #42b983;
  border-left: 3px solid #42b983;
}
.content {
  flex: 1;
  /* ✅ flex布局核心修复 */
  min-height: 0;
  padding: 20px;
  background-color: #f5f7fa;
  /* ✅ 只有内容区域内部滚动 */
  overflow-y: auto;
}
</style>
