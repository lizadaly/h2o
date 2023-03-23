<template>
    <section>
<<<<<<< HEAD
        <search-form v-on:search-results="onSearchResults" />
        <result-form v-bind:search-results="results" />
=======
        <search-form />
        <result-form />
>>>>>>> 9d9448d3b20d9a0b52c8a2e18970099b507d82fb
    </section>
</template>

<script>
import SearchForm from './SearchForm'; 
import ResultForm from './ResultForm';

export default {
    components: {
        SearchForm,
        ResultForm
<<<<<<< HEAD
    },
    data: () => ({
        results: [],
    }),
    methods: {
        onSearchResults: function(res) {
            this.results = res
        }
=======
>>>>>>> 9d9448d3b20d9a0b52c8a2e18970099b507d82fb
    }
}
</script>

