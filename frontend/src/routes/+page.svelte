<script>
    import Translator from "./components/Translator.svelte"
    import LogosTelegram from '~icons/logos/telegram'
</script>

<div class="w-full h-full flex items-center justify-center">
  <div class="w-[min(50rem,90%)] 3xl:w-[70rem]">
    <Translator/>

    <section class="my-5 bg-white shadow-default p-5 md:p-6 rounded-xl text-[0.95rem] leading-relaxed text-gray-800">
      <h2 class="font-semibold mb-3 text-lg">Бесплатный онлайн‑переводчик бурятского языка</h2>
      <div class="space-y-2">
        <p>
          На нашем сайте вы можете бесплатно переводить с бурятского на русский и с русского на бурятский язык.
        </p>
        <p>
          В отличие от онлайн‑словарей, сервис переводит целые предложения и тексты.
        </p>
        <p>
          В основе переводчика — собственная нейросеть, разработанная с учётом особенностей бурятского языка.
        </p>
        <p>
          По нашим проверкам на текущий момент качество перевода выше, чем у альтернатив. Тем не менее автоматический перевод может содержать неточности.
        </p>
      </div>
    </section>

    <section class="my-5 bg-white shadow-default p-5 md:p-6 rounded-xl text-[0.95rem] leading-relaxed text-gray-800">
      <div class="flex items-center justify-between">
        <p>
          Есть идеи или нашли ошибку? 
          <a href="https://t.me/burtranslate" target="_blank" rel="noopener noreferrer" class="underline text-blue-600 hover:text-blue-700">Напишите нам!</a>
        </p>
        <a href="https://t.me/burtranslate" target="_blank" rel="noopener noreferrer" class="ml-2" aria-label="Открыть чат в Telegram">
          <LogosTelegram class="text-xl" aria-hidden="true" focusable="false"/>
        </a>
      </div>
    </section>
  </div>
</div>
