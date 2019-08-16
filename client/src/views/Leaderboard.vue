<template>
  <div class="hero-section">
    <section class="container">
      <div class="row justify-content-center mt-5 mb-1">
        <div class="col-10 text-center">
          <b-table striped hover dark id="anigen-leaderboard" :sort-desc.sync="sortDesc" :sort-by.sync="sortBy" :items="items" :per-page="perPage" :current-page="currentPage" :fields="fields">
            <template slot="actions" slot-scope="row">
              <b-button :disabled="upvoting(row.item.anigen_titles)" variant="success" size="md" @click="upVoteExcellent(row.item.anigen_titles)">
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
          <b-pagination v-model="currentPage" :total-rows="rows" :per-page="perPage" align="center" aria-controls="anigen-leaderboard"></b-pagination>
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
      perPage: 10,
      currentPage: 1,
      sortBy: 'votes',
      sortDesc: true,
      items: [],
      upvoted: [],
      fields: [
        { key: 'anigen_titles', label: 'Top Anigen Titles', sortable: true },
        { key: 'votes', label: 'Number of Votes', sortable: true },
        { key: 'actions', label: 'Actions' },
      ],
    };
  },

  async created() {
    await this.fetchLeaders();
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

    fetchLeaders() {
      this.toggleBusy();

      const path = 'http://anigen-dev.us-east-1.elasticbeanstalk.com:80/api/leaderboard';

      axios.get(path)
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

    async upVoteExcellent(anigen_title) {
      const path = `http://anigen-dev.us-east-1.elasticbeanstalk.com:80/api/leaderboard/?upvote=${anigen_title}`;

      await axios.get(path)
        .then((response) => {
          console.log(response.data);
          this.upvoted.push(anigen_title);
          this.fetchLeaders();
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
