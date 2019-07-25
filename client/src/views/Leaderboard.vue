<template>
	<div>
		<section class="container">
			<div class="row justify-content-center">
				<div class="col-10 text-center">
					<b-table striped hover
					id="anigen-leaderboard"
					:sort-desc.sync="sortDesc"
					:sort-by.sync="sortBy"
					:items="items"
					:per-page="perPage"
					:current-page="currentPage"
					:fields="fields"
					>
						<template slot="actions" slot-scope="row">
							<b-button :disabled="upvoting(row.item.anigen_titles)" variant="success" size="md" @click="upVoteExcellent(row.item.anigen_titles)">
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
					aria-controls="anigen-leaderboard"
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
				perPage: 10,
				currentPage: 1,
				sortBy: "votes",
				sortDesc: true,
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

			await this.fetchLeaders();

		},

		methods: {

			upvoting(title) {
				if (this.upvoted.includes(title)) {
					return true;
				}
				return false;
			},

			fetchLeaders() {
				const path_leaderboard = 'http://localhost:5000/leaderboard';
				axios.get(path_leaderboard)
				.then((response) => {
					this.items = response.data;
					console.log(response.data);
				})
				.catch((error) => {
					console.log(error);
				});
			},

			async upVoteExcellent(anigen_title) {
				const path = `http://localhost:5000/leaderboard/?upvote=${anigen_title}`;
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
