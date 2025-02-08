// 1. 导入Vue Router模块
import { createRouter, createWebHashHistory } from 'vue-router'
import NProgress from "../config/nprogress";
import { useUserStore } from '../store/modules/user'
import { useMenuStore } from '../store/modules/menu'
// 2. 定义一些路由,每个路由都需要映射到一个组件。
// 定义静态路由
export const staticRouter = [
    {
        path: '/',
        redirect: "/login",
        isMenu: false
    },
    {
        path: '/login',
        name: 'Login',
        meta: { title: '后台管理系统 - 登录'},
        component: ()=> import('../views/login/Login.vue'),
        isMenu: false

    },
    {
        path: '/index',
        name: 'index',
        component: ()=> import('../views/layout/Index.vue'),
        redirect: "/home",
        isMenu: true,
        funcNode:1,
        children: [{
            path: '/home',
            name: 'home',
            meta: { title: '首页', icon: 'HomeFilled',affix: true },
            component: ()=> import('../views/home/Index.vue')
        }]
    },
    {
        path: '/user',
        name: 'UserSetting',
        redirect: '/user/usersetting',
        component: ()=> import('../views/layout/Index.vue'),
        isMenu: true,
        funcNode: 1,
        children: [
            {
                path: 'usersetting',
                name: 'usersettings',
                meta: { title: '个人设置', icon: 'Stamp'},
                component: ()=> import('../views/usersettings/Index.vue')
            }
        ]
    }
]
// 定义动态路由
export const asyncRoutes = [
    {
        path: '/set',
        name: 'SetSetting',
        meta: { title: '系统设置', icon: 'Tools', role: ['ROLE_ADMIN']},
        redirect: '/set/setting',
        component: ()=> import('../views/layout/Index.vue'),
        isMenu: true,
        funcNode: 1,
        children: [
            {
                path: 'setting',
                name: 'settings',
                meta: { title: '系统设置', icon: 'Tools', role: ['ROLE_ADMIN']},
                component: ()=> import('../views/settings/Index.vue')
            }
        ]
    },
    {
        path: '/system',
        name: 'system',
        meta: {
            title: '用户管理',
            icon: 'UserFilled',
            role: ['ROLE_ADMIN']
        },
        redirect: '/system/user',
        component: ()=> import('../views/layout/Index.vue'),
        isMenu: true,
        funcNode:2,
        children: [
            {
                path: 'user',
                name: 'User',
                meta: {
                    title: '用户管理',
                    icon: 'User',
                    role: ['ROLE_ADMIN']
                },
                component: ()=> import('../views/user/UserList.vue')
            },
            {
                path: 'role',
                name: 'Role',
                meta: {
                    title: '角色管理',
                    icon: 'Medal',
                    role: ['ROLE_ADMIN']
                },
                component: ()=> import('../views/role/RoleList.vue')
            }
        ]
    },
    {
        path: '/foods',
        name: 'foods',
        meta: {
            title: '菜单管理',
            icon: 'Menu',
            role: ['ROLE_USER','ROLE_ADMIN']
        },
        redirect: '/foods/index',
        component: ()=> import('../views/layout/Index.vue'),
        isMenu: true,
        funcNode:2,
        children: [
            {
                path: 'index',
                name: 'foodsIndex',
                meta: {
                    title: '菜品列表信息',
                    icon: 'Food',
                    role: ['ROLE_USER','ROLE_ADMIN']
                },
                component: ()=> import('../views/foods/Index.vue')
            },
            {
                path: 'order',
                name: 'orderIndex',
                meta: {
                    title: '订单列表信息',
                    icon: 'Finished',
                    role: ['ROLE_USER','ROLE_ADMIN']
                },
                component: ()=> import('../views/order/Index.vue')
            }
        ]
    },
]

// 3. 创建路由实例并传递 `routes` 配置
const router = createRouter({
    // 4. 内部提供了 history 模式的实现。为了简单起见，我们在这里使用 hash 模式。
    history: createWebHashHistory(),
    routes: staticRouter
})
// 路由拦截 beforeEach
router.beforeEach(async (to, from, next) => {
// 1.NProgress 开始
    NProgress.start();

    //2.如果是访问登录页，直接放行
    if(to.path==='/login')return next()

    //3.判断是否有Token,没有重定向到login
    const userStore = useUserStore()
    if(!userStore.token)return next({path:`/login?redirect=${to.path}`,replace:true})

    // 获取登录用户的角色
    const { role } = userStore
    const roles = []
    if ( role === 1 ) {
        roles.push("ROLE_ADMIN")
    } else {
        roles.push("ROLE_USER")
    }
    // 根据角色动态生成路由访问映射
   const menuStore = useMenuStore()
    if (!menuStore.routers.length) {
        const accessRoutes = menuStore.generateRoutes({roles: roles})
        accessRoutes.forEach(item => router.addRoute(item)) // 动态添加访问路由表
        next({ ...to, replace: true }) // 这里相当于push到一个页面 不在进入路由拦截
    }else {
        // 正常访问页面
        next();
    }
});
/**
 * @description 路由跳转结束
 * */
router.afterEach(() => {
    NProgress.done();
});
/**
 * @description 路由跳转错误
 * */
router.onError(error => {
    NProgress.done();
    console.warn("路由错误", error.message);
});
export default router
