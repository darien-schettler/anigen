<template>
	<footer class="footer bg-white text-white">
		<section class="container-fluid py-4 px-5">
			<div class="row justify-content-between">
				<div class="col-lg-7 my-auto py-3">
					<div class=row>
						<div class="col-lg-7 py-3 my-auto text-center">
							<h3 class="font-weight-bold text-dark my-auto">Hiring ?  Looking to Start a Project ?</h3>
						</div>
						<div class="col-lg-4 py-3 my-auto text-center">
							<button v-b-modal.modal-contact-form type="button" class="btn btn-outline-light font-weight-bold px-3 bulma-teal py-2 rounded-lg shadow-sm" style="font-size: 28px">Let's Talk</button>
						</div>
					</div>
					<b-modal id="modal-contact-form" size="xl" title="Let's Talk!">
						<div class="container-fluid">
							<b-form @submit="onSubmit" @reset="onReset" v-if="show">
								<div class="row">
									<div class="col-md-12">
										<b-form-group class="font-weight-bold"
										id="input-group-email"
										label="Email address:"
										label-for="input-email"
										>
											<b-form-input
											id="input-email"
											v-model="form.email"
											type="email"
											required
											placeholder="Enter email"
											></b-form-input>
										</b-form-group>
									</div>
								</div>
								<div class="row">
									<div class="col-md-6">
										<b-form-group class="font-weight-bold" id="input-group-firstname" label="First Name:" label-for="input-fn">
											<b-form-input
											id="input-fn"
											v-model="form.first_name"
											required
											placeholder="John"
											></b-form-input>
										</b-form-group>
									</div>
									<div class="col-md-6">
										<b-form-group class="font-weight-bold" id="input-group-lastname" label="Last Name:" label-for="input-ln">
											<b-form-input
											id="input-ln"
											v-model="form.last_name"
											required
											placeholder="Doe"
											></b-form-input>
										</b-form-group>
									</div>
								</div>
								<div class="row">
									<div class="col-12">
										<b-form-group class="font-weight-bold" id="input-group-textarea" label="Your Message:" label-for="input-textarea">
											<b-form-textarea
										    id="input-textarea"
										    v-model="form.emailText"
										    placeholder="Your message to me goes here..."
										    rows="2"
										    max-rows="6"
										    ></b-form-textarea>
										</b-form-group>
									</div>
								</div>
							</b-form>
						</div>
						<template slot="modal-footer" slot-scope="{ ok, cancel}">
					      <!-- Emulate built in modal footer ok and cancel button actions -->

					      <b-button  variant="outline-warning" class="font-weight-bold mr-auto mr-3 px-3" @click="onReset($event)">
					        Reset Fields
					      </b-button>

  					      <b-button  variant="outline-danger" type="reset" class="font-weight-bold mr-2 px-3" @click="cancel(); onReset($event)">
					        Cancel
					      </b-button>
					      <b-button  variant="outline-success" type="submit" class="font-weight-bold ml-3 px-4" @click="ok(); onSubmit($event);">
					        Send It
					      </b-button>
					     </template>
					</b-modal>
				</div>
				<div class="col-lg-4 py-3">
					<div class="row">
						<div class="col-lg-5 py-3 my-auto text-center">
							<a href="https://github.com/darien-schettler/" title="Github" class="font-weight-bold"><img height="50px" class="px-1 thumbnail " src="@/assets/icons/Github.svg"/></a>
							<a href="https://www.linkedin.com/in/darien-schettler-bb0a5086/" title="LinkedIn" class="font-weight-bold"><img height="50px" class="px-1 thumbnail " src="@/assets/icons/Linkedin.svg"/></a>
							<a href="https://www.reddit.com/user/darien-schettler" title="Reddit" class="font-weight-bold"><img height="50px" class="px-1 thumbnail " src="@/assets/icons/Reddit.svg"/></a>
						</div>
						<div class="col-lg-7 py-4 my-auto text-center">
							<a href="darienschettler.com" class="bulma-teal font-weight-bold shadow-sm py-4 px-3 rounded-lg" style="font-size: 20px; text-decoration: none !important;" title="Portfolio">My Portfolio:
								<img height="50px" class="thumbnail px-3 mb-2" src="@/assets/icons/portfolio.jpg"/>
							</a>
						</div>
					</div>
				</div>
			</div>
		</section>
	</footer>
</template>

<script>
export default {

  name: 'Footer',

  data() {
    return {
      form: {
        email: '',
        first_name: '',
        last_name: '',
        emailText: '',
      },
      show: true,
    };
  },

  methods: {

    onSubmit(evt) {
      evt.preventDefault();
      alert(JSON.stringify(this.form));
    },

    onReset(evt) {
      evt.preventDefault();
      // Reset our form values
      this.form.email = '';
      this.form.first_name = '';
      this.form.last_name = '';
      this.form.emailText = '';

      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
};
</script>

<style lang="scss">
.bulma-teal{
	color: lighten(#00D1B2, 0.7);
	&:hover {
        color:teal;
    }
   }
   .thumbnail {
  display: inline-block;
  vertical-align: middle;
  -webkit-transform: perspective(1px) translateZ(0);
  transform: perspective(1px) translateZ(0);
  box-shadow: 0 0 1px transparent;
  -webkit-transition-duration: 0.35s;
  transition-duration: 0.35s;
  -webkit-transition-property: transform;
  transition-property: transform;
}
.thumbnail:hover, .thumbnail:focus, .thumbnail:active {
  -webkit-transform: scale(1.175);
  transform: scale(1.175);
}

</style>
