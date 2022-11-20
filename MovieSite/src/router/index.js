import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/home.vue'
import Login from '../components/login.vue'
import Register from '../components/register.vue'
import Movies from '../components/movies.vue'
import ManageMovies from '../components/manage-movies.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    },
    {
        path: '/movies',
        name: 'Movies',
        component: Movies
    },
    {
        path: '/manage-movies',
        name: 'ManageMovies',
        component: ManageMovies
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router