<template>
  <div class="hero-section">
    <section class="container">
      <div class="row justify-content-center my-4">
        <div class="col-10 text-center">
          <b-table striped hover dark id="anigen-weirderboard" :sort-desc.sync="sortDesc" :sort-by.sync="sortBy" :items="items" :per-page="perPage" :current-page="currentPage" :fields="fields">
            <template slot="actions" slot-scope="row">
              <b-button :disabled="upvoting(row.item.anigen_titles)" variant="success" size="md" @click="upVoteWeird(row.item.anigen_titles)">
                Upvote
              </b-button>
            </template>
            <div slot="table-busy" class="text-center my-2">
              <div>
                <b-spinner variant="light" class="align-middle"></b-spinner>
                <strong class="text-light px-1">Loading Anigen Titles ...</strong>
              </div>
            </div>
          </b-table>
        </div>
      </div>
      <div class="row justify-content-center">
        <div class="col-4">
          <b-pagination v-model="currentPage" :total-rows="rows" :per-page="perPage" align="center" aria-controls="anigen-weirderboard"></b-pagination>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import axios from 'axios';

export default {

  name: 'Home',

  data() {
    return {
      isBusy: false,
      myToggle: false,
      perPage: 10,
      sortBy: 'votes',
      sortDesc: true,
      currentPage: 1,
      items: [],
      upvoted: [],
      fields: [
        { key: 'anigen_titles', label: 'Strange Anigen Titles', sortable: true },
        { key: 'votes', label: 'Number of Votes', sortable: true },
        { key: 'actions', label: 'Actions' },
      ],
    };
  },

  async created() {
    await this.fetchWeird();
  },

  methods: {
    toggleBusy() {
      this.isBusy = !this.isBusy;
    },
    upvoting(title) {
      if (this.upvoted.includes(title)) {
        return true;
      }
      return false;
    },

    fetchWeird() {
      this.toggleBusy();

      const path_weirderboard = 'http://localhost:80/api/weirderboard';
      axios.get(path_weirderboard)
        .then((response) => {
          this.items = response.data;
          this.toggleBusy();
          console.log(response.data);
        })
        .catch((error) => {
          this.toggleBusy();
          console.log(error);
        });
    },

    async upVoteWeird(anigen_title) {
      const path = `http://localhost:80/api/weirderboard/?upvote=${anigen_title}`;
      await axios.get(path)
        .then((response) => {
          console.log(response.data);
          this.fetchWeird();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },

  },

  computed: {

    rows() {
      return this.items.length;
    },

  },

};

</script>
<style>
</style>
