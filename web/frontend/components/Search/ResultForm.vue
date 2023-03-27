<template>
  <ol>
    <li v-if="searchResults.length > 0">
      <span class="name">Case</span>
      <span class="cite">Citation</span>
      <span class="date">Effective date</span>
      <span class="source">Source</span>
    </li>
    <li
      v-for="r in searchResults"
      @click="() => add(r.id)"
      :data-doc-id="r.id"
      :key="r.id"
      class="results-entry"
      role="button"
      tabindex="0"
    >
      <span class="name" :title="r.fullName">{{ r.shortName }}</span>
      <span class="cite" :title="r.fullCitations">{{ r.shortCitations }}</span>
      <span class="date">{{ r.effectiveDate }}</span>
      <span class="source">
        <a
          target="_blank"
          title="Open in the Case Law Access Project"
          :href="r.url"
          >CAP</a
        >
      </span>
    </li>
  </ol>
</template>

<script>
export default {
  props: {
    searchResults: Array,
  },
  methods: {
    add: function (id) {
      this.$emit('add-doc', id)
    },
  },
};
</script>

<style lang="scss" scoped>
ol {
  padding: 0;
  list-style-type: none;
  font-size: 16px;

  li:first-of-type {
    font-weight: bold;

    &:hover,
    &:focus-within {
      background: none;
    }
  }

  li + li {
    border-top: 0.5px solid rgb(149, 149, 149);
  }

  li {
    display: flex;
    flex-wrap: nowrap;
    justify-content: space-between;

    align-items: center;
    padding: 0.5em;

    &:hover,
    &:focus-within {
      background: hsl(43, 94%, 80%);
    }

    .name {
      flex-basis: 30%;
    }

    .cite {
      flex-basis: 40%;
    }

    .date {
      flex-basis: 10ch;
    }

    a {
      text-decoration: underline !important;
      text-underline-offset: 4px;
    }

    a:after {
      content: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAQElEQVR42qXKwQkAIAxDUUdxtO6/RBQkQZvSi8I/pL4BoGw/XPkh4XigPmsUgh0626AjRsgxHTkUThsG2T/sIlzdTsp52kSS1wAAAABJRU5ErkJggg==);
      margin: 0 0 0 0.5em;
    }
  }
}
</style>