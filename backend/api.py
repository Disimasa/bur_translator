from fastapi import FastAPI, Body
from starlette.middleware.cors import CORSMiddleware
from translator import get_translator
import asyncio

print('create app')
app = FastAPI()
print('start loading model')
translator = get_translator()
print('finished loading model')
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def root():
    return {'Hello': 'world'}


@app.post('/translate/rus_bur')
async def translate_rus_bur(text: str = Body(..., embed=True)):
    loop = asyncio.get_event_loop()
    translation = await loop.run_in_executor(None, translator.translate, text)

    return {'text': text, 'translation': translation}


@app.post('/translate/bur_rus')
async def translate_bur_rus(text: str = Body(..., embed=True)):
    loop = asyncio.get_event_loop()
    translation = await loop.run_in_executor(None, translator.translate, text, 'bxr_Cyrl', 'rus_Cyrl')

    return {'text': text, 'translation': translation}
