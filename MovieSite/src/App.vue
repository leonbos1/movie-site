<template>
  <div class="container">
      <ul>
        <li><a class="active" href="/">Home</a></li>
        <li><a href="/movies">Movies</a></li>
        <li><a  href="/register">Register</a></li>
        <li><a  href="/login">Login</a></li>

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
    };
  },
  mounted() {
  },
  methods: {
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
