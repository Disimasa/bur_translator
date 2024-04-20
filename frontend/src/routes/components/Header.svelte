<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@300..700&display=swap" rel="stylesheet">

<script>
  import logo from '$lib/images/logo.svg'

  let darkMode = false

  function switchTheme() {
    darkMode = !darkMode;

    darkMode
      ? document.documentElement.classList.add('dark')
      : document.documentElement.classList.remove('dark');

    console.log('qwe')
  }
</script>

<div class="w-full flex items-center h-20 p-4">
  <img src={logo} class="mr-1.5 "/>
  <h1 class="leading-5 font-comfortaa text-sm font-bold">Русско-бурятский
      <br>
      переводчик</h1>
</div>
