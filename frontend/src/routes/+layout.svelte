<script>
  import '../app.css'
  import Header from "./components/Header.svelte";
</script>

<div class="w-full min-h-full bg-white dark:bg-black flex flex-col">
  <Header/>
  <main class="flex-1 w-full h-full">
    <slot/>
  </main>
</div>
