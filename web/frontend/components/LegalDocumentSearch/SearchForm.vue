<template>
  <form class="form-group case-search"
    @submit.prevent="search">
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
      :disabled="pending"
    />
    
    
    <button class="advanced-search-toggle" @click="toggleAdvanced">Advanced search</button>

    <fieldset class="advanced-search">
      <label>
        Source:
          <select class="form-control" v-model="searchLimit">
            <option :value="null">All sources</option>
            <option :value="source" v-for="source in getSources" :key="source.id">{{source.name}}</option>
          </select>
      </label>
      <label>
        Jurisdiction:
        <select class="form-control" v-model="jurisdiction" name="jurisdiction">
          <option :value="j.val" v-for="j in jurisdictions" :key="j.val">{{ j.name }}</option>
        </select>
      </label>
      <label>
            Decision Date
            <div class="date-row form-control-inline">
                <input
                  name="after_date"
                  type="date"
                  class="form-control"
                  placeholder="YYYY-MM-DD"
                  v-model="after_date"
                  />
              <span> - </span>
              <input
                  name="before_date"
                  type="date"
                  class="form-control"
                  placeholder="YYYY-MM-DD"
                  v-model="before_date"
                  />
            </div>
        </label>
        <p>
          {{searchLimit ? searchLimit.long_description : ''}}
        </p>
    </fieldset>
  </form>
</template>

<script>
import url from "../../libs/urls";

 const api = url.url("search_using");

export default {
  data: () => ({
    pending: false,
    query: "",
    jurisdictions: [
  { val: "", name: "All jurisdictions" },
  { val: "ala", name: "Alabama" },
  { val: "alaska", name: "Alaska" },
  { val: "am-samoa", name: "American Samoa" },
  { val: "ariz", name: "Arizona" },
  { val: "ark", name: "Arkansas" },
  { val: "cal", name: "California" },
  { val: "colo", name: "Colorado" },
  { val: "conn", name: "Connecticut" },
  { val: "dakota-territory", name: "Dakota Territory" },
  { val: "dc", name: "District of Columbia" },
  { val: "del", name: "Delaware" },
  { val: "fla", name: "Florida" },
  { val: "ga", name: "Georgia" },
  { val: "guam", name: "Guam" },
  { val: "haw", name: "Hawaii" },
  { val: "idaho", name: "Idaho" },
  { val: "ill", name: "Illinois" },
  { val: "ind", name: "Indiana" },
  { val: "iowa", name: "Iowa" },
  { val: "kan", name: "Kansas" },
  { val: "ky", name: "Kentucky" },
  { val: "la", name: "Louisiana" },
  { val: "mass", name: "Massachusetts" },
  { val: "md", name: "Maryland" },
  { val: "me", name: "Maine" },
  { val: "mich", name: "Michigan" },
  { val: "minn", name: "Minnesota" },
  { val: "miss", name: "Mississippi" },
  { val: "mo", name: "Missouri" },
  { val: "mont", name: "Montana" },
  { val: "native-american", name: "Native American" },
  { val: "navajo-nation", name: "Navajo Nation" },
  { val: "nc", name: "North Carolina" },
  { val: "nd", name: "North Dakota" },
  { val: "neb", name: "Nebraska" },
  { val: "nev", name: "Nevada" },
  { val: "nh", name: "New Hampshire" },
  { val: "nj", name: "New Jersey" },
  { val: "nm", name: "New Mexico" },
  { val: "n-mar-i", name: "Northern Mariana Islands" },
  { val: "ny", name: "New York" },
  { val: "ohio", name: "Ohio" },
  { val: "okla", name: "Oklahoma" },
  { val: "or", name: "Oregon" },
  { val: "pa", name: "Pennsylvania" },
  { val: "pr", name: "Puerto Rico" },
  { val: "ri", name: "Rhode Island" },
  { val: "sc", name: "South Carolina" },
  { val: "sd", name: "South Dakota" },
  { val: "tenn", name: "Tennessee" },
  { val: "tex", name: "Texas" },
  { val: "tribal", name: "Tribal jurisdictions" },
  { val: "uk", name: "United Kingdom" },
  { val: "us", name: "United States" },
  { val: "utah", name: "Utah" },
  { val: "va", name: "Virginia" },
  { val: "vi", name: "Virgin Islands" },
  { val: "vt", name: "Vermont" },
  { val: "wash", name: "Washington" },
  { val: "wis", name: "Wisconsin" },
  { val: "w-va", name: "West Virginia" },
  { val: "wyo", name: "Wyoming" }
]
  }),
  methods: {
    search: async function () {
      this.pending = true;
      const url = api({ sourceId: 1 }) + '?' + new URLSearchParams({q: this.query}) // FIXME use multiple sources
      const resp = await fetch(url);
      const results = await resp.json(); 
      this.$emit("search-results", results.results);
      this.pending = false;      
    },
  },
};
</script>

<style lang="scss" scoped>
form {
  display: flex;
  flex-wrap: wrap;
  margin: 30px auto 30px 0 !important;
  justify-content: space-between;
  align-items: center;
  gap: 1em;

  input {
    margin: 0 !important;
  }
  input[type="text"] {
    flex-basis: 66%;
  }
  button.advanced-search-toggle {
    background: none;
    border: none;
    text-decoration: underline;
    text-underline-offset: 4px;
    padding: 0;
  }
  
  button.advanced-search-toggle {
    background: none;
    border: none;
    text-decoration: underline;
    text-underline-offset: 4px;
    padding: 0;
  }
  .advanced-search {
    display: flex;
    gap: 1em;
    flex-wrap: wrap;
    margin: 1em 0;

    label {
      width: 100%;
      line-height: 2em;
      
      & * {
        font-weight: normal;
      }
      select {
        padding-left: .5em;
      }
    }
    & > div {
      flex-basis: 24%;
    }
    & > label {
      flex-basis: 48%;
    }
    .form-control {
      font-size: 16px;
      height: initial;
    }
    p {
      flex-basis: 100%;
    }
  }
}

</style>