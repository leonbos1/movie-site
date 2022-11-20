<template>
  <div class="container">
      <ul>
        <li><a class="active" href="/">Home</a></li>
        <li><a href="/movies">Movies</a></li>
        <li><a href="/manage-movies">Manage Movies</a></li>
        <li><a href="/manage-users">Manage Users</a></li>
        <li v-if="!loggedIn"><a  href="/register">Register</a></li>
        <li  v-if="!loggedIn"><a  href="/login">Login</a></li>
        <li v-if="loggedIn" ><a @click="logout">Logout</a></li>

      </ul>
 
    <div class="content">
      <router-view />
  
    </div>
  </div>
</template>

<script>

export default {
  name: "App",
  data: function () {
    return {
      loggedIn: false,
      url: "http://192.168.178.69:1500",
    };
  },
  mounted() {
    this.checkLogin();
  },
  methods: {
    checkLogin() {
      let token = localStorage.getItem("token");
      fetch(this.url + "/v1/checklogin", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "token": token,
        },
      })
        .then((response) => {
          if (response.status == 200) {
            this.loggedIn = true;
          } else {
            this.loggedIn = false;
          }
        });      
    },

    logout() {
    //TODO logout to api?
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    window.location.href = "/";
    this.loggedIn = false;
  },
  },

  
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}

.container {
  width: 100%;
  text-align: center;
  margin: 0 auto;
  margin-top: 0px;
}

.content {
  width: 100%;
  text-align: center;
  margin: 0 auto;
}

@media (min-width: 480px) {
  .content {
    width: 80%;
  }
}

ul {
  list-style-type: none;
  padding: 0;
  overflow: hidden;
  background-color: #272727;
  position: relative;
  margin-top: 0;
  
}

li {
  float: left;
}

li a {
  display: block;
  color: white;
  text-align: center;
  padding: 18px 20px;
  text-decoration: none;
}

li a:hover:not(.active) {
  background-color: #111;
}

.active {
  background-color: #0043d3;
}

body, html {
    margin:0;
}

.right {
  position: absolute;
  right: 0;
  top: 0;
}
</style>
