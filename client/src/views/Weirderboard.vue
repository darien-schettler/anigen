<template>
  <div class="bg-light">
    <section class="container">
      <div class="row justify-content-center">
        <div class="col-10 text-center">
          <b-table striped hover
          id="anigen-weirderboard"
          :sort-desc.sync="sortDesc"
          :sort-by.sync="sortBy"
          :items="items"
          :per-page="perPage"
          :current-page="currentPage"
          :fields="fields"
          >
            <template slot="actions" slot-scope="row">
               <b-button :disabled="upvoting(row.item.anigen_titles)" variant="success" size="md" @click="upVoteWeird(row.item.anigen_titles)">
                Upvote
              </b-button>
            </template>
          </b-table>
        </div>
      </div>
      <div class="row justify-content-center">
        <div class="col-4">
          <b-pagination
            v-model="currentPage"
            :total-rows="rows"
            :per-page="perPage"
            align="center"
            aria-controls="anigen-weirderboard"
          ></b-pagination>
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
      myToggle: false,
      perPage: 10,
      sortBy: 'votes',
      sortDesc: true,
      currentPage: 1,
      items: [],
      upvoted: [],
      fields: [
        { key: 'anigen_titles', label: 'Anigen Titles', sortable: true },
        { key: 'votes', label: 'Number of Votes', sortable: true },
        { key: 'actions', label: 'Actions' },
      ],
    };
  },

  async created() {
    await this.fetchWeird();
  },

  methods: {

    upvoting(title) {
      if (this.upvoted.includes(title)) {
        return true;
      }
      return false;
    },

    fetchWeird() {
      const path_weirderboard = 'http://localhost:80/api/weirderboard';
      axios.get(path_weirderboard)
        .then((response) => {
          this.items = response.data;
          console.log(response.data);
        })
        .catch((error) => {
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
