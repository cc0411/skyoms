// Vue
import Vue from 'vue'
import i18n from './i18n'
import App from './App'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
// 核心插件
import d2Admin from '@/plugin/d2admin'
// store
import store from '@/store/index'
// elementui
import ElementUI from 'element-ui'
Vue.use(ElementUI)
// v-charts
import VCharts from 'v-charts'
Vue.use(VCharts)
//h-charts
import HighchartsVue from 'highcharts-vue'
Vue.use(HighchartsVue)

// 菜单和路由设置
import router from './router'
import menuHeader from '@/menu/header'
import menuAside from '@/menu/aside'
import util from '@/libs/util.js'

// 核心插件
Vue.use(d2Admin)
// 从后台获取动态路由
util.router.init(router)

new Vue({
  router,
  store,
  i18n,
  render: h => h(App),
  created () {
    // 处理路由 得到每一级的路由设置
    // this.$store.commit('d2admin/page/init', frameInRoutes)
    // 设置顶栏菜单
    this.$store.commit('d2admin/menu/headerSet', menuHeader)
    // 设置侧边栏菜单，改为从后台获取
    // this.$store.commit('d2admin/menu/asideSet', menuAside)
    util.menu.init()
    // 初始化菜单搜索功能
    // this.$store.commit('d2admin/search/init', menuHeader)
    this.$store.commit('d2admin/search/init', menuAside)
  },
  mounted () {
    // 展示系统信息
    this.$store.commit('d2admin/releases/versionShow')
    // 用户登录后从数据库加载一系列的设置
    this.$store.dispatch('d2admin/account/load')
    // 获取并记录用户 UA
    this.$store.commit('d2admin/ua/get')
    // 初始化全屏监听
    this.$store.dispatch('d2admin/fullscreen/listen')
  }
}).$mount('#app')
