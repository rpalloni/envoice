import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import "bulma/css/bulma.css"

// configure default url for axios to backend server
axios.defaults.baseURL = 'http://127.0.0.1:8000'

// configure root component
createApp(App)
    .use(store)
    .use(router, axios)
    .mount('#app') // mount the app in the browser DOM via public/index.html <div id="app"></div>


// create app >> mount in the DOM
