<template>
  <div>
    <form v-on:submit="loginMethod" class="login-form">
      <div class="form-group">
        <input
          type="text"
          v-model="username"
          class="form-control"
          placeholder="Enter username"
        />
      </div>
      <div class="form-group">
        <input
          type="password"
          v-model="password"
          class="form-control"
          placeholder="Password"
        />
      </div>
      <button class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>
  
<script>
export default {
  name: "LoginPage",

  data: function () {
    return {
      username: "",
      password: "",
      url: "http://192.168.178.69:1500"
    };
  },

  components: {},

  methods: {
    loginMethod(e) {
      e.preventDefault();
      fetch(this.url + "/v1/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      })
        .then((response) => response.json())
        //.then((data) => data.text())
        .then((data) => {
          localStorage.setItem("token", data["token"]);
          localStorage.setItem("username", data["user"]);
          window.location.href = "/";
        });
    },
  },
};
</script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style lang="scss" scoped>
.login-form {
  width: 50%;
  margin: 0 auto;
}
</style>
   