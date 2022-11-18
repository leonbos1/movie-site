<template>
    <div>
        <form v-on:submit="registerMethod" class="login-form">
            <div class="form-group">
                <input type="text" v-model="username" class="form-control" placeholder="Enter username">
            </div>
            <div class="form-group">
                <input type="password" v-model="password" class="form-control" placeholder="Password">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
  </template>
  
  <script>
  
  export default {
  
    name: "RegisterPage",

    data: function () {
        return {
            username: "",
            password: "",
            url: "http://192.168.178.69:1500"
        };
      },
  
    components: {
    },

    methods: {
        registerMethod(e) {
            e.preventDefault();
            fetch(this.url + "/v1/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: this.username,
                password: this.password,
            }),
        })
            
        },
    }
  };
  </script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style lang="scss" scoped>
  .login-form {
    width: 50%;
    margin: 0 auto;
  }

  </style>
   