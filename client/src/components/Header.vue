<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
      <b-navbar-brand class="ml-5" href="/">Anigen</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto mr-5">
          <b-nav-item class="px-1" href="/">Home</b-nav-item>
          <b-nav-item class="px-1" href="/leaderboard">Leaderboard</b-nav-item>
          <b-nav-item class="px-1" href="/weirderboard">Weirderboard</b-nav-item>
          <b-nav-item class="pl-4" href="/about">About</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: 'Header',
};
</script>

<style>
</style>
