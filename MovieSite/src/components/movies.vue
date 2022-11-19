<template>
  <div></div>
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
            console.log(this.movies);
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
</style>
   