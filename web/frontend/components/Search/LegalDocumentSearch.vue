<template>
  <section>
    <search-form @search-results="onSearchResults" />
    <result-form @add-doc="onAddDoc" :search-results="results" />
  </section>
</template>

<script>
import SearchForm from "./SearchForm";
import ResultForm from "./ResultForm";
import url from "../../libs/urls";
import { get_csrf_token } from '../../legacy/lib/helpers';

const docImport = url.url('from_source');
//const docAdd = url.url('new_legal_doc');

export default {
  props: {
    casebook: String
  },
  components: {
    SearchForm,
    ResultForm,
  },
  data: () => ({
    results: [],
  }),
  methods: {
    onSearchResults: function (res) {
      this.results = res;
    },
    onAddDoc: async function (resourceId) {
      const resp = await fetch(docImport({sourceId: 1}), {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRF-Token": get_csrf_token()
        },
        body: JSON.stringify({id: resourceId})
    })
    console.log(resp)

//      const addUrl = this.docAddUrl({casebookId: this.casebook});
    },
  },
};
</script>

