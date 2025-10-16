<script lang="ts">
  import { Circle } from 'svelte-loading-spinners'
  import { fade } from 'svelte/transition'
  import Button from "./Button.svelte"
  import axios from 'axios'
  import { toast } from "svelte-sonner"

  let inputText = ''
  let translationText = ''
  let translationLoading = false
  let translationDirection: 'rus_bur' | 'bur_rus' = 'rus_bur'
  let inputDom: HTMLTextAreaElement

  function addSymbol(symbol: string) {
    const start = inputDom.selectionStart
    inputDom.setRangeText(symbol)
    inputDom.focus()
    const newPos = start + symbol.length;
    inputDom.selectionStart = inputDom.selectionEnd = newPos
    inputText = inputDom.value
  }

  function changeTranslationDirection() {
    translationDirection = translationDirection === 'rus_bur' ? 'bur_rus' : 'rus_bur'
    inputText = ''
    translationText = ''
  }

  async function translate() {
    // Скрыть мобильную клавиатуру, если фокус на поле ввода
    if (inputDom && typeof inputDom.blur === 'function') {
      inputDom.blur()
    }
    if (translationLoading) {
      toast.warning('Дождитесь окончания загрузки')
      return
    }

    if (!inputText) {
      toast.warning('Введите текст для перевода')
      return
    }

    translationLoading = true

    translationText = await axios.post('/translate', {
      translationDirection,
      inputText
    }, {timeout: 180000}).then(async res => await res.data)
      .catch(err => {
        toast.error('Ошибка при переводе! ' + err)
        return ''
      })


    translationLoading = false
  }

  async function handleEnter(event: KeyboardEvent) {
    if (event.key == 'Enter' && !event.shiftKey) {
      event.preventDefault()
      // Скрыть мобильную клавиатуру при нажатии Enter
      if (inputDom && typeof inputDom.blur === 'function') {
        inputDom.blur()
      }
      await translate()
    }
  }

</script>

<div class="rounded-3xl shadow-default mt-10 p-4">
  <div class="w-full flex items-center text-center pb-3 border-b" class:flex-row-reverse={translationDirection === 'bur_rus'}>
    <p class="w-1/2">РУССКИЙ</p>
    <button on:click={changeTranslationDirection} aria-label="Поменять направление перевода">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 48 48">
        <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M42 19H6M30 7l12 12M6.799 29h36m-36 0l12 12" />
      </svg>
    </button>
    <p class="w-1/2">БУРЯТСКИЙ</p>
  </div>

  <div class="flex flex-col md:flex-row flex-wrap">
    <label for="input-text" class="sr-only">Текст для перевода</label>
    <textarea id="input-text" bind:this={inputDom} on:keydown={handleEnter}
        placeholder="Введите текст"
        class="min-h-[10rem] min-w-[15rem] flex-1 resize-none p-4 bg-transparent border-0 outline-none order-1 md:order-1"
        maxlength="1000"
        enterkeyhint="done"
        bind:value={inputText}
    ></textarea>

    <div class="border-t mx-2 md:border-r md:my-2 order-3 md:order-2 flex-0"></div>

    <div class="min-h-[10rem] min-w-[15rem] flex-1 order-4 md:order-3 flex items-center justify-center p-4 relative">
      {#if translationLoading}
        <div class="m-auto"><Circle size="40" color="rgb(96 165 250)" /></div>
      {:else}
        <label for="output-text" class="sr-only">Результат перевода</label>
        <textarea id="output-text"
            class="absolute w-full h-full resize-none border-0 outline-none p-4"
            readonly
            bind:value={translationText}
        ></textarea>
      {/if}
    </div>

    <div class="w-full flex justify-between items-center mt-2 order-2 md:order-4 mb-3 md:mb-0">
      {#if translationDirection === 'bur_rus'}
        <div class="flex" transition:fade={{duration: 200}}>
          <Button class="rounded-lg px-2 pb-1 mr-2" aria-label="Вставить букву ү" on:click={() => addSymbol('ү')}>ү</Button>
          <Button class="rounded-lg px-2 pb-1 mr-2" aria-label="Вставить букву һ" on:click={() => addSymbol('һ')}>һ</Button>
          <Button class="rounded-lg px-2 pb-1" aria-label="Вставить букву ө" on:click={() => addSymbol('ө')}>ө</Button>
        </div>
      {/if}
      <Button on:click={translate} class="py-2 px-6" aria-label="Выполнить перевод">Перевести</Button>
    </div>

  </div>

</div>