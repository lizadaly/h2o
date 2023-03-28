<template>
  <section>
    <search-form @search-results="onSearchResults" />
    <result-form @add-doc="onAddDoc" :search-results="results" :added="added"/>
  </section>
</template>

<script>
import SearchForm from "./SearchForm";
import ResultForm from "./ResultForm";
import url from "../../libs/urls";
import { get_csrf_token } from '../../legacy/lib/helpers';

const api = url.url('legal_document_resource_view');

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
    added: undefined,
  }),
  methods: {
    reset: function () {
      this.results = [];
      this.added = undefined;
    },
    onSearchResults: function (res) {
      this.reset();
      this.results = res;
    },
    onAddDoc: async function (sourceRef) {
      this.added = undefined;
      const resp = await fetch(api({casebookId: this.casebook}), {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRF-Token": get_csrf_token()
        },
        body: JSON.stringify({source_id: 1, source_ref: sourceRef})
      })
      const body = await resp.json();
      this.added = {
        resourceId: body.resource_id,
        redirectUrl: body.redirect_url,
        sourceRef
      }
      console.log(body)

    },
  },
};
</script>

