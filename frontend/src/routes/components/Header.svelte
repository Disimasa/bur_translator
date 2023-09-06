<script>
  let darkMode = false

  function switchTheme() {
    darkMode = !darkMode;

    darkMode
      ? document.documentElement.classList.add('dark')
      : document.documentElement.classList.remove('dark');

    console.log('qwe')
  }
</script>

<div class="w-full flex justify-between h-20 p-4">
  <h1>Переводчик</h1>
</div>
