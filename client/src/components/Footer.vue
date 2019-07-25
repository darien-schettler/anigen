<template>
<footer class="footer bg-white text-white">
	<section class="container py-4">
		<div class="row justify-content-between">
			<div class="col-lg-8 my-auto">
				<h3 class="font-weight-bold text-dark my-auto">Hiring ?  Looking to Start a Project ? <span class="bulma-teal px-3"> Let's Talk ✉</span></h3>
			</div>
			<div class="col-lg-3">
				<a href="https://github.com/darien-schettler/" title="Github" class="font-weight-bold"><img height="50px" class="px-1" src="@/assets/icons/Github.svg"/></a>
				<a href="https://www.linkedin.com/in/darien-schettler-bb0a5086/" title="LinkedIn" class="font-weight-bold"><img height="50px" class="px-1" src="@/assets/icons/Linkedin.svg"/></a>
				<a href="https://www.reddit.com/user/darien-schettler" title="Reddit" class="font-weight-bold"><img height="50px" class="px-1" src="@/assets/icons/Reddit.svg"/></a>
			</div>
			
		</div>
	</section>
</footer>

</template>

<script>
export default {
  name: 'Footer',
};
</script>

<style lang="scss">
.bulma-teal{
	color: lighten(#00D1B2, 0.7);
}
</style>
