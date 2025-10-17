<script lang="ts">
  import { Circle } from 'svelte-loading-spinners'
  import { fade } from 'svelte/transition'
  import Button from "./Button.svelte"
  import { toast } from "svelte-sonner"
  import { apiFetch } from '$lib/api'

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
    await apiFetch('/translate', { body: JSON.stringify({ translationDirection, inputText})})
      .then(result => translationText = result)
      .catch(err => {
        toast.error('Ошибка при переводе! ' + err)
        translationText = ''
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
    <button on:click={changeTranslationDirection} title="Поменять направление перевода" aria-label="Поменять направление перевода" class="group">
      <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 48 48" aria-hidden="true" focusable="false">
        <!-- Верхняя стрелка вправо -->
        <g class="transform transition-transform duration-200 ease-out group-hover:translate-x-2">
          <path d="M8 16h28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M28 8l8 8l-8 8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </g>
        <!-- Нижняя стрелка влево -->
        <g class="transform transition-transform duration-200 ease-out group-hover:-translate-x-2">
          <path d="M40 32H12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          <path d="M20 24l-8 8l8 8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </g>
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