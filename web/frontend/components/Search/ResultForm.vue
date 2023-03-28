<template>
  <ol :class="resultId ? 'adding': ''">
    <li v-if="searchResults.length > 0">
      <span class="name">Case</span>
      <span class="cite">Citation</span>
      <span class="date">Effective date</span>
      <span class="source">Source</span>
    </li>
    <li
      v-for="r in searchResults"
        @click="(e) => add(e.target.closest('li'), r.id)"
        :data-doc-id="r.id"
        :data-result-selected="r.id === resultId"
        :data-result-added="added && r.id === added.sourceRef"
        :key="r.id"
        :disabled="!!resultId"
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
      <span class="added-message" v-if="added && r.id === added.sourceRef">
        This document has been added to your casebook.
        
        <a :href="added.redirectUrl">Edit your new resource</a>, 
        <a>search again</a>, or close this window.
      </span>
    </li>
  </ol>
</template>

<script>
export default {
  props: {
    searchResults: Array,
    added: Object,
  },
  data: () => ({
    resultId: undefined,
    adding: false
  }),
  methods: {
    add: function (row, id) {
      if (row.getAttribute("disabled")) {
        return;
      }
      row.classList.toggle('adding')
      this.resultId = id
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
  &.adding {
    
    li:not([data-result-selected]) {
        opacity: 0.5;
    }

    li:hover,
    li:focus-within {
      background: inherit;
    }
    li[data-result-selected] {
      background: hsl(43, 94%, 80%);
      cursor: wait;
    }
    li[data-result-added] {
      background: hsl(117, 43%, 80%);
      cursor: auto;
    }
  }

  li {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    padding: 0.5em;

    &:hover,
    &:focus-within {
      background: hsl(43, 94%, 80%);
    }
    &[disabled] {
      cursor: not-allowed;
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
    .added-message {
      flex-basis: 100%;
      margin: auto;
      display: inline-flex;
      padding: 1em;
      text-align: center;
    }
    a {
      text-decoration: underline !important;
      text-underline-offset: 4px;
    }
    a[href^="http"]:after {
      content: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAQElEQVR42qXKwQkAIAxDUUdxtO6/RBQkQZvSi8I/pL4BoGw/XPkh4XigPmsUgh0626AjRsgxHTkUThsG2T/sIlzdTsp52kSS1wAAAABJRU5ErkJggg==);
      margin: 0 0 0 0.5em;
    }
  }
}
</style>