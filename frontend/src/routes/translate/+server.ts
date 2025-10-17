import { BACKEND_URL } from '$env/static/private'
import { json, error } from '@sveltejs/kit'
import {apiFetch} from "$lib/api"

export async function POST({ request }) {
  const { translationDirection, inputText } = await request.json()

  try {
    const res = await apiFetch(
      `${BACKEND_URL}/translate/${translationDirection}/`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText })
      }
    )
    return json(res.translation)
  } catch (err) {
    return json({ error: err || 'Ошибка перевода' }, { status: 400 })
  }
}