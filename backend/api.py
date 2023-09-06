from fastapi import FastAPI, Body
from starlette.middleware.cors import CORSMiddleware

from translator import get_rus_bur_translator

app = FastAPI()

origins = ['https://bur-translator.vercel.app/']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def cache_models():
    get_rus_bur_translator()


@app.get('/')
def root():
    return {'Hello': 'world'}


@app.post('/translate/rus_bur')
async def translate_rus_bur(text: str = Body(..., embed=True)):
    rus_bur_translator = get_rus_bur_translator()
    translation = rus_bur_translator.translate(text)
    return {'text': text, 'translation': translation}
