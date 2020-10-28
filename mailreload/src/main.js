// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ElementUI);

Vue.config.productionTip = false
import serverurlvaluefromjs from '@/config/serverurlvalue'
import VueClipboard from 'vue-clipboard2'
Vue.use(VueClipboard)

import VueDOMPurifyHTML from 'vue-dompurify-html'
Vue.use(VueDOMPurifyHTML)

import Ads from 'vue-google-adsense'
 
Vue.use(require('vue-script2'))
 
Vue.use(Ads.Adsense)
Vue.use(Ads.InArticleAdsense)
Vue.use(Ads.InFeedAdsense)

// 本地服务器地址
Vue.prototype.serviceurl = function () {
  // 正式环境value值取空
  // let serviceurlvalue = ''
  let serviceurlvalue = serverurlvaluefromjs.serverurl
  return serviceurlvalue
}

var _hmt = _hmt || [];
window._hmt = _hmt; // 修改为window 全局变量
 (function () {
       var hm = document.createElement("script");
       hm.src = "https://hm.baidu.com/hm.js?f17073ce3910dee882c81b53f3128a8f";
      //  hm.src = "https://hm.baidu.com/hm.js?6547945c1c0cdcbb1814a71a7ccbee38";
       var s = document.getElementsByTagName("script")[0];
       s.parentNode.insertBefore(hm, s);
  })();

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
