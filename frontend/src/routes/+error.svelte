<script>
  import { page } from '$app/stores'
</script>

<div class="w-full h-full flex items-center justify-center p-6">
  <div class="max-w-xl w-full text-center bg-white dark:bg-black shadow-default rounded-2xl p-8">
    <h1 class="text-2xl font-bold mb-2">{$page.status === 404 ? 'Страница не найдена' : 'Ошибка!'}</h1>
    <p class="text-gray-600 dark:text-gray-300 mb-6">
      {$page.status === 404
        ? 'Кажется, такой страницы нет. Проверьте адрес или вернитесь на главную.'
        : ($page.error?.message || 'Произошла непредвиденная ошибка.')}
    </p>
    <div class="flex items-center justify-center gap-4">
      <a href="/" class="py-2 px-4 rounded-lg bg-blue-500 text-white hover:bg-blue-600">На главную</a>
      <a href="https://t.me/burtranslate" target="_blank" rel="noopener noreferrer" class="underline">Написать в Telegram</a>
    </div>
  </div>
  
</div>


