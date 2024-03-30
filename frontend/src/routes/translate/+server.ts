import { BACKEND_URL } from '$env/static/private'
import { json, error } from '@sveltejs/kit'
import axios from 'axios'

export async function POST({ request }) {
  const { translationDirection, inputText } = await request.json()

  const response = await axios.post(`${BACKEND_URL}/translate/${translationDirection}/`, {
    text: inputText
  }).then(async res => await res.data)
    .catch(err => { console.log(err); throw error(500, 'Ошибка при переводе')})

  return json(response?.translation)
}