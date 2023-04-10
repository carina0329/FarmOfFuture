 //root component to list the routing parts
const routes=[
    {path:'/',component:home},
    {path:'/sensor',component:sensor},
    {path:'/map',component:map}
]

const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes, // short for `routes: routes`
  })

// const app = new Vue({
//     router
// }).$mount('#app')

// 5. Create and mount the root instance.
const app = Vue.createApp({})
// Make sure to _use_ the router instance to make the
// whole app router-aware.
app.use(router)

app.mount('#app')