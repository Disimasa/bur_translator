<script>
  import '../app.css'
  import Header from "./components/Header.svelte";
  import { Toaster } from 'svelte-sonner'
</script>

<div class="w-full min-h-full bg-white dark:bg-black flex flex-col">
  <Toaster position="top-right" visibleToasts="1" duration={2000} richColors />
  <Header/>
  <main class="flex-1 w-full h-full">
    <slot/>
  </main>
</div>
