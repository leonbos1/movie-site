<template>
  <div>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>username</th>
          <th>password</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td><input v-model="user.username" /></td>
          <td><input v-model="user.password" /></td>
          <td>
            <button @click="editUser(user.id)">Edit</button>
            <button @click="deleteUser(user.id)">Delete</button>
          </td>
        </tr>

        <tr>
          <td></td>
          <td><input v-model="newUser.username" /></td>
          <td><input v-model="newUser.password" /></td>
          <td>
            <button @click="addUser()">Add</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
  
<script>
export default {
  name: "UsersPage",

  data: function () {
    return {
      url: "http://192.168.178.69:1500",
      users: [],
      currentPage: 1,
      newUser: {
        username: "",
        password: "",
      },
    };
  },

  components: {},

  methods: {
    getUsers() {
      fetch(this.url + "/v1/users", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          token: localStorage.getItem("token"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.users = data;
        });
    },

    addUser() {
      fetch(this.url + "/v1/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          token: localStorage.getItem("token"),
        },
        body: JSON.stringify({
          username: this.newUser.username,
          password: this.newUser.password,
        }),
      })
        .then(() => {
          this.getUsers();
        });
    },

    editUser(id) {
      let user = this.users.find((user) => user.id == id);
      fetch(this.url + "/v1/users", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          token: localStorage.getItem("token"),
        },
        body: JSON.stringify({
          id: user.id,
          username: user.username,
          password: user.password,
        }),
      }) 
        .then(() => {
          this.getUsers();
        });
    },

    deleteUser(id) {
      fetch(this.url + "/v1/users", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          token: localStorage.getItem("token"),
        },
        body: JSON.stringify({
          id: id,
        }),
      })
        .then(() => {
          this.getUsers();
        });
    },
  },
  mounted() {
    this.getUsers();
  },
};
</script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
.card {
  margin-bottom: 20px;
}

.card-img-top {
  width: 100%;
  height: 15vw;
  object-fit: cover;
}

.card-text {
  height: 100px;
  overflow: hidden;
}

.card-title {
  height: 50px;
  overflow: hidden;
}
</style>
   