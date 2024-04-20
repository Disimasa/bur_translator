<script lang="ts">
  import Icon from 'svelte-icons-pack/Icon.svelte'
  import CgArrowsExchange from 'svelte-icons-pack/cg/CgArrowsExchange'
  import { Circle } from 'svelte-loading-spinners'
  import { fade } from 'svelte/transition'
  import Button from "./Button.svelte"
  import axios from 'axios'
  import { toast } from "svelte-sonner"

  let inputText = ''
  let translationText = ''
  let translationLoading = false
  let translationDirection: 'rus_bur' | 'bur_rus' = 'rus_bur'

  function addSymbol(event, symbol) {
    event.preventDefault()
    inputText += symbol
  }

  function changeTranslationDirection() {
    translationDirection = translationDirection === 'rus_bur' ? 'bur_rus' : 'rus_bur'
    inputText = ''
    translationText = ''
  }

  async function translate() {
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
    }).then(async res => await res.data)
      .catch(err => { alert('Ошибка при переводе!'); return ''})


    translationLoading = false
  }

  async function handleEnter(event) {
    if(event.keyCode===13) {
      event.preventDefault()
      await translate()
    }
  }

</script>
<svelte:window on:keydown={handleEnter} />
<div class="w-[45rem] rounded-3xl shadow-default mt-10 mx-7 p-4">
  <div class="w-full flex items-center text-center pb-3 border-b" class:flex-row-reverse={translationDirection === 'bur_rus'}>
    <p class="w-1/2">РУССКИЙ</p>
    <button on:click={changeTranslationDirection}><Icon src={CgArrowsExchange} size="25"/></button>
    <p class="w-1/2">БУРЯТСКИЙ</p>
  </div>

  <div class="flex flex-col md:flex-row flex-wrap">
    <textarea
        placeholder="Введите текст"
        class="min-h-[10rem] min-w-[15rem] flex-1 resize-none p-4 bg-transparent border-0 outline-none order-1 md:order-1"
        maxlength="200"
        bind:value={inputText}
    ></textarea>

    <div class="border-t mx-2 md:border-r md:my-2 order-3 md:order-2 flex-0"></div>

    <div class="min-h-[10rem] min-w-[15rem] flex-1 order-4 md:order-3 flex items-center justify-center p-4 relative">
      {#if translationLoading}
        <Circle size="40" color="rgb(96 165 250)" class="m-auto" />
      {:else}
        <textarea
            class="absolute w-full h-full resize-none border-0 outline-none p-4"
            readonly
            bind:value={translationText}
        ></textarea>
      {/if}
    </div>

    <div class="w-full flex justify-between items-center mt-2 order-2 md:order-4 mb-3 md:mb-0">
      {#if translationDirection === 'bur_rus'}
        <div class="flex" transition:fade={{duration: 200}}>
          <Button class="rounded-lg px-2 pb-1 mr-2" on:click={event => addSymbol(event, 'ү')}>ү</Button>
          <Button class="rounded-lg px-2 pb-1 mr-2" on:click={event => addSymbol(event, 'һ')}>һ</Button>
          <Button class="rounded-lg px-2 pb-1" on:click={event => addSymbol(event, 'ө')}>ө</Button>
        </div>
      {/if}
      <Button on:click={translate} class="py-2 px-6">Перевести</Button>
    </div>

  </div>
</div>