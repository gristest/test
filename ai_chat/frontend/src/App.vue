<template>
  <div id="app">
    <h1>App组件已加载</h1>
    <p>当前路由: {{ $route.path }}</p>
    <p>路由匹配: {{ $route.matched.length }}</p>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  padding: 20px;
}
</style>