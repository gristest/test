<template>
  <div style="padding: 20px; text-align: center;">
    <h1>路由测试页面</h1>
    <p>如果你能看到这个页面，说明Vue Router工作正常</p>
    <button @click="count++">点击次数: {{ count }}</button>
  </div>
</template>

<script>
export default {
  name: 'SimpleTest',
  data() {
    return {
      count: 0
    }
  }
}
</script>