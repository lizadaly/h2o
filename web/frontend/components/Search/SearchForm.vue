<template>
  <form class="form-group case-search"
    v-on:submit.prevent="search">
    <input
      type="text"
      class="form-control"
      placeholder="Search for a case or section of federal code"
      v-model="query"
    />
    <input
      type="submit"
      class="save-button"
      :value="pending ? 'Searching...' : 'Search'"
    />
  </form>
</template>

<script>
import url from "../../libs/urls";

const api = url.url("search_using");

export default {
  data: () => ({
    pending: false,
    query: "",
  }),
  methods: {
    search: async function () {
      this.pending = true;
      const url = api({ sourceId: 1 });
      const resp = await fetch(url);
      const results = await resp.json();
      this.$emit("search-results", results);
      this.pending = false;      
    },
  },
};
</script>

<style lang="scss" scoped>
form {
  display: flex;
  flex-wrap: wrap;
  margin: auto;
  justify-content: space-between;
  align-items: center;
  gap: 1em;

  input {
    margin: 0 !important;
  }
  input[type="text"] {
    flex-basis: 66%;
  }
}
</style>