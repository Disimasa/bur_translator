<script>
    import Translator from "./components/Translator.svelte"
    import LogosTelegram from '~icons/logos/telegram'
</script>

<div class="w-full h-full flex items-center justify-center">
  <div class="w-[min(50rem,90%)] 3xl:w-[70rem]">
    <Translator/>

    <div class="flex items-center justify-between my-5 bg-white font-comfortaa shadow-default p-4 rounded-xl">
      <p class="">
      Есть идеи или нашли ошибку? <a href="https://t.me/burtranslate" target="_blank" class="underline text-blue-400">Напишите нам!</a>
    </p>
      <a href="https://t.me/burtranslate" target="_blank" class="ml-2">
        <LogosTelegram class="text-xl"/>
      </a>
    </div>
  </div>
</div>
