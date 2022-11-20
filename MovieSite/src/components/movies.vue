<template>
  <div>
    <h1>Movies</h1>
    <div class="row">
      <div class="col-md-3" v-for="movie in movies" :key="movie.id">
        <div class="card">
          <img :src="movie.image" class="card-img-top" alt="..." />
          <div class="card-body">
            <h5 class="card-title">{{ movie.title }}</h5>
            <p class="card-text">{{ movie.description }}</p>
            <p class="card-text">{{ movie.year }}</p>
          </div>
        </div>
      </div>
    </div>
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
  width: 20vw;
  height: 20vh;
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

.row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.col-md-3 {
  flex: 0 0 25%;
  max-width: 25%;
}

</style>
   