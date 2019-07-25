<template>
  <div id="app">
    <router-view id="app-header" name="header" />
    <router-view id="app-body"/>
    <router-view id="app-footer" name="footer" />
  </div>
</template>

<style lang="scss">
	#app-body{
		min-height: 90vh !important;
	}
	html {
    	height: 100%;
	}
</style>
