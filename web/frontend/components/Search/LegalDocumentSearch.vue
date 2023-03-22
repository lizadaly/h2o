<template>
    <section>
        <search-form />
        <result-form />
    </section>
</template>

<script>
import SearchForm from './SearchForm'; 
import ResultForm from './ResultForm';

export default {
    components: {
        SearchForm,
        ResultForm
    }
}
</script>

