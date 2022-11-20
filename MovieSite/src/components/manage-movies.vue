<template>
  <div>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>Description</th>
          <th>Year</th>
          <th>Image</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="movie in movies" :key="movie.id">
          <td>{{ movie.id }}</td>
          <td><input v-model="movie.title" /></td>
          <td><input v-model="movie.description" /></td>
          <td><input v-model="movie.year" /></td>
          <td>
            <input type="file" @change="onFileChange(movie.id, $event)" />
          </td>
          <td>
            <button @click="editMovie(movie.id)">Edit</button>
            <button @click="deleteMovie(movie.id)">Delete</button>
          </td>
        </tr>

        <tr>
          <td></td>
          <td><input v-model="newMovie.title" /></td>
          <td><input v-model="newMovie.description" /></td>
          <td><input v-model="newMovie.year" /></td>
          <td>
            <input type="file" @change="onFileChange(null, $event)" />
          </td>
          <td>
            <button @click="addMovie()">Add</button>
          </td>
        </tr>

      </tbody>
    </table>
  </div>
</template>
  
<script>
export default {
  name: "MoviePage",

  data: function () {
    return {
      url: "http://192.168.178.69:1500",
      movies: [],
      currentPage: 1,
      newMovie: {
        title: "",
        description: "",
        year: "",
        image: "",
      },
    };
  },

  components: {},

  methods: {
    fetchMovies() {
      fetch(this.url + "/v1/movies?page=" + this.currentPage)
        .then((response) => response.json())
        .then((data) => {
          this.movies = data;
        })
    },

    addMovie() {
      fetch(this.url + "/v1/movies", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.newMovie),
      })
        .then(() => {
          this.fetchMovies();
        })
    },

    onFileChange(id, event) {
      var file = event.target.files[0];
      var reader = new FileReader();
      reader.readAsDataURL(file);

      var movie = this.movies.find((movie) => movie.id == id);

      reader.onload = () => {
        if (movie) {
          movie.image = reader.result;
        } else {
          this.newMovie.image = reader.result;
        }
      };
    },

    editMovie(id) {
      var movie = this.movies.find((movie) => movie.id == id);

      fetch(this.url + "/v1/movies", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": localStorage.getItem("token"),
        },
        body: JSON.stringify({
          id: id,
          title: movie.title,
          description: movie.description,
          year: movie.year,
          image: movie.image,
        }),
      })
        .then(() => this.fetchMovies())
    },

    deleteMovie(id) {
      fetch(this.url + "/v1/movies", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": localStorage.getItem("token"),
        },
        body: JSON.stringify({
          id: id,
        }),
      })
        .then(() => this.fetchMovies())
    },

  },
  mounted() {
    this.fetchMovies();
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
   