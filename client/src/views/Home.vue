<template>
  <div class="hero-section">
    <section class="container">
      <div class="row pt-3 my-2 mx-5 justify-content-center">
        <div class="col-sm-4 text-center">
          <b-button variant="outline-light" class="mx-3 my-1 shadow-sm font-weight-bold" @click="getTitles(50)">Generate 1 Title</b-button>
        </div>
        <div class="col-sm-4 text-center">
          <b-button variant="outline-light" class="mx-3 my-1 shadow-sm font-weight-bold" @click="getTitles(250)">Generate Small Batch of Titles</b-button>
        </div>
        <div class="col-sm-4 text-center">
          <b-button variant="outline-light" class="mx-3 my-1 shadow-sm font-weight-bold" @click="getTitles(1000)">Generate Large Batch of Titles</b-button>
        </div>
      </div>
      <div class="row pb-5 pt-2 justify-content-center">
        <div class="col-6 text-center">
          <b-button v-b-toggle.collapse-advanced-options size="sm" variant="secondary" class="px-3 py-2 font-weight-bold shadow-sm">Advanced Options</b-button>
          <b-collapse id="collapse-advanced-options" class="mt-2">
            <b-card>
              <div class="row justify-content-center">
                <div class="col-12 text-center">
                  <label for="range-randomness" class="font-weight-bold">Randomness : {{ randomness }}</label>
                  <b-form-input id="range-randomness" v-model="randomness" type="range" min="0.1" max="2" step="0.025"></b-form-input>
                </div>
              </div>
              <div class="row justify-content-center my-3">
                <div class="col-3 text-center my-auto">
                  <label for="input-start-string" class="font-weight-bold">Seed String : </label>
                </div>
                <div class="col-8 text-center ml-1">
                  <b-form-input id="input-start-string" v-model="startString" placeholder="..."></b-form-input>
                </div>
              </div>
            </b-card>
          </b-collapse>
        </div>
      </div>
      <div v-show="visible" class="row justify-content-center">
        <div class="col-10 text-center">
          <b-table striped hover dark id="anigen-table" :items="titles" :per-page="perPage" :current-page="currentPage" :busy="isBusy" :fields="fields">
            <template slot="actions" slot-scope="row">
              <b-button :disabled="excellentClick(row.item.anigen_title)" variant="success" size="sm" @click="markExcellent(row.item)" class=mr-2>
                Excellent
              </b-button>
              <b-button :disabled="weirdClick(row.item.anigen_title)" variant="danger" size="sm" @click="markWeird(row.item)">
                Weird
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
      <div v-show="visible" class="row justify-content-center">
        <div class="col-4">
          <b-pagination v-model="currentPage" :total-rows="rows" :per-page="perPage" align="center" aria-controls="anigen-table"></b-pagination>
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
      visible: false,
      perPage: 8,
      currentPage: 1,
      randomness: '0.75',
      startString: '',
      titles: [],
      dropped_titles: [],
      excellentTitles: [],
      weirdTitles: [],
      fields: [
        { key: 'anigen_title', label: 'Anigen Titles', sortable: true },
        { key: 'actions', label: 'Actions' },
      ],
    };
  },

  methods: {

    toggleBusy() {
      this.isBusy = !this.isBusy;
    },

    excellentClick(title) {
      if (this.excellentTitles.includes(title)) {
        return true;
      }
      return false;
    },

    weirdClick(title) {
      console.log(title);
      if (this.weirdTitles.includes(title)) {
        return true;
      }
      return false;
    },

    async getTitles(batchSize) {
      this.toggleBusy();
      this.visible = true;

      const path = 'http://anigen-dev.us-east-1.elasticbeanstalk.com:80/api/predict/';
      await axios.post(path, {
          batchSize,
          randomness: this.randomness,
          startString: this.startString,
        })
        .then((response) => {
          this.titles = response.data[0];
          this.dropped_titles = response.data[1];
          console.log(response.data);
          this.toggleBusy();
        })
        .catch((error) => {
          // eslint-disable-next-line
          this.toggleBusy();
          console.error(error);
        });
    },

    async markExcellent(anigen_title) {
      const path = `http://anigen-dev.us-east-1.elasticbeanstalk.com:80/api/leaderboard/?title=${anigen_title.anigen_title}`;

      await axios.get(path)
        .then((response) => {
          this.excellentTitles.push(anigen_title.anigen_title);
          console.log(response.data);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },

    async markWeird(anigen_title) {
      const path = `http://anigen-dev.us-east-1.elasticbeanstalk.com:80/api/weirderboard/?title=${anigen_title.anigen_title}`;

      await axios.get(path)
        .then((response) => {
          this.weirdTitles.push(anigen_title.anigen_title);
          console.log(response.data);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },

  },

  computed: {

    rows() {
      return this.titles.length;
    },

  },

};

</script>
<style>
@media all and (min-width: 1000px) {
  .hero-section {
    min-height: 100vh;
    background-image: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)),
      url("../assets/images/cowboybebop_topcrop.jpg");
    /* flex-box thing */
    display: flex;
    flex-direction: column;
    background-size: cover;
  }
}

@media all and (max-width: 1000px) {
  .hero-section {
    min-height: 100vh;
    background-image: linear-gradient(rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.75)),
      url("../assets/images/cowboybebop_half_res.jpg");
    /* flex-box thing */
    display: flex;
    flex-direction: column;
    background-size: cover;
  }
}

</style>
