import Vue from 'vue';
import Router from 'vue-router';
import Ping from './components/Ping.vue';
import Stocks from './components/Stocks.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Stocks',
      component: Stocks,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});
