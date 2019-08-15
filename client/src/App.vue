<template>
  <div id="app">
    <link href="https://fonts.googleapis.com/css?family=Megrim|Raleway:200,400&display=swap" rel="stylesheet">
    <router-view id="app-header" name="header" />
    <router-view id="app-body"/>
    <router-view id="app-footer" name="footer" />
  </div>
</template>

<style lang="scss">
	#app-body {
		min-height: 92.5vh !important;
    font-family: 'Raleway', sans-serif;
	}
  #app-footer {
    font-family: 'Raleway', sans-serif;
  }
  #app-header {
    font-family: 'Raleway', sans-serif;
  }
  #modal-contact-form{
    font-family: 'Raleway', sans-serif !important;
  }
	html {
    	height: 100%;
	}
</style>
