<template>
    <ol>
        <li v-for="r in searchResults" :key="r.id" class="results-entry" role="button">
            <span class="name" :title="r.fullName">{{ r.shortName }}</span>
            <span class="cite" :title="r.fullCitations">{{ r.shortCitations }}</span>
            <span class="date">{{ r.effectiveDate }}</span>
            <span class="source">CAP</span>
        </li>
    </ol>
    
</template>

<script>
export default {
    props: {
        searchResults: Array
    }
}
</script>

<style lang="scss" scoped>
ol {
    padding: 0;
    list-style-type: none;
    font-size: 16px;
    li + li {
        border-top: 0.5px solid rgb(149, 149, 149);
    }
    li {
        display: flex;
        flex-wrap: nowrap;
        justify-content: space-between;

        align-items: center;
        padding: .5em 0;

        &:hover {
            background: lightblue;
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

    }
}
</style>