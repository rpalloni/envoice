/*
sync URLs to app views
*/

import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import SignUp from '../views/SignUp.vue'
import LogIn from '../views/LogIn.vue'
import Account from '../views/dashboard/Account.vue'
import Dashboard from '../views/dashboard/Dashboard.vue'
import Clients from '../views/dashboard/ClientsList.vue'
import Client from '../views/dashboard/ClientDetails.vue'
import ClientAdd from '../views/dashboard/ClientAdd.vue'
import ClientEdit from '../views/dashboard/ClientEdit.vue'
import TeamEdit from '../views/dashboard/TeamEdit.vue'
import Invoices from '../views/dashboard/InvoicesList.vue'
import Invoice from '../views/dashboard/InvoiceDetails.vue'
import InvoiceAdd from '../views/dashboard/InvoiceAdd.vue'

import store from '../store'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/login',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/account',
    name: 'Account',
    component: Account,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/clients',
    name: 'Clients',
    component: Clients,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/clients/:id', // dynamic router >> params: { id: client.cl_id }
    name: 'Client',
    component: Client,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/clients/add',
    name: 'ClientAdd',
    component: ClientAdd,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/clients/:id/edit', // dynamic router >> params: { id: client.cl_id }
    name: 'ClientEdit',
    component: ClientEdit,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/account/edit-team', // dynamic router >> params: { id: team.tm_id }
    name: 'TeamEdit',
    component: TeamEdit,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/invoices',
    name: 'Invoices',
    component: Invoices,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/invoices/:id', // dynamic router >> params: { id: invoice.iv_id }
    name: 'Invoice',
    component: Invoice,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/dashboard/invoices/add',
    name: 'InvoiceAdd',
    component: InvoiceAdd,
    meta: {
      requireLogin: true
    }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router
