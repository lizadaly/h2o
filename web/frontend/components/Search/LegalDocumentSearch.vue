<template>
    <section>
        <search-form v-on:search-results="onSearchResults" />
        <result-form v-bind:search-results="results" />
    </section>
</template>

<script>
import SearchForm from './SearchForm'; 
import ResultForm from './ResultForm';

export default {
    components: {
        SearchForm,
        ResultForm
    },
    data: () => ({
        results: [],
    }),
    methods: {
        onSearchResults: function(res) {
            this.results = res
        }
    }
}
</script>

