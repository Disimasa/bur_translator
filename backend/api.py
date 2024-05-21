from fastapi import FastAPI, Body
from starlette.middleware.cors import CORSMiddleware
from backend.translator import translator

app = FastAPI()

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
    translation = translator.translate(text)
    return {'text': text, 'translation': translation}


@app.post('/translate/bur_rus')
async def translate_bur_rus(text: str = Body(..., embed=True)):
    translation = translator.translate(text, src_lang='bxr_Cyrl', tgt_lang='rus_Cyrl')
    return {'text': text, 'translation': translation}
