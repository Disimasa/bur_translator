export async function apiFetch(url: string, options = {}, timeout: number = 1_200_000) {
  return fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    ...options,
    signal: AbortSignal.timeout(timeout),
  })
    .then(async res => {
      const json = await res.json()
      return res.ok ? json : Promise.reject(json.error || 'Ошибка сервера')
    })
    .catch(err => {
      if (err.name === 'TimeoutError') {
        return Promise.reject('Превышено время ожидания ответа от сервера. Ограничение в 20 минут')
      }
      return Promise.reject(err.message || err)
    })
}
