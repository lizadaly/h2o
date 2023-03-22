<template>
  <form class="form-group case-search">
    <input
      name="q"
      type="text"
      class="form-control"
      placeholder="Search for a case or section of federal code"
    />
    <input type="submit" class="save-button" :value="pending ? 'Searching...' : 'Search'" />
  </form>
</template>

<script>
export default {
  data: () => ({
    pending: false,
  }),
};
</script>

<style lang="css" scoped>
form {
  display: flex;
  flex-wrap: wrap;
  margin: auto;
  justify-content: space-between;
  align-items: center;
  gap: 1em;
}
</style>