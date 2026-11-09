import { ElMessage } from 'element-plus'

// 统一美化配置
const defaultOption = {
  duration: 2200, // 自动关闭时间 ms
  offset: 60,     // 距离页面顶部距离
  showClose: true // 显示关闭按钮
}

// 封装四个方法
const message = {
  success(msg) {
    return ElMessage({
      message: msg,
      type: 'success',
      customClass: 'my-message-success',
      ...defaultOption
    })
  },
  error(msg) {
    return ElMessage({
      message: msg,
      type: 'error',
      customClass: 'my-message-error',
      ...defaultOption
    })
  },
  warning(msg) {
    return ElMessage({
      message: msg,
      type: 'warning',
      customClass: 'my-message-warning',
      ...defaultOption
    })
  },
  info(msg) {
    return ElMessage({
      message: msg,
      type: 'info',
      customClass: 'my-message-info',
      ...defaultOption
    })
  }
}

export default message