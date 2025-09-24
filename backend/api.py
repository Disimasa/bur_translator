from fastapi import FastAPI, Body, HTTPException
from starlette.middleware.cors import CORSMiddleware
from translator import get_translator
import asyncio
import gc
import torch
import logging
import psutil

# Настройка логирования только для ошибок
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

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
    try:
        # Ограничиваем длину входного текста
        if len(text) > 2000:
            raise HTTPException(status_code=400, detail="Text too long. Maximum 2000 characters allowed.")
        
        loop = asyncio.get_event_loop()
        translation = await loop.run_in_executor(None, translator.translate, text)
        
        # Принудительная очистка памяти после каждого запроса
        gc.collect()
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
        
        return {'text': text, 'translation': translation}
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        # Очистка памяти даже при ошибке
        gc.collect()
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@app.post('/translate/bur_rus')
async def translate_bur_rus(text: str = Body(..., embed=True)):
    try:
        # Ограничиваем длину входного текста
        if len(text) > 2000:
            raise HTTPException(status_code=400, detail="Text too long. Maximum 2000 characters allowed.")
        
        loop = asyncio.get_event_loop()
        translation = await loop.run_in_executor(None, translator.translate, text, 'bxr_Cyrl', 'rus_Cyrl')
        
        # Принудительная очистка памяти после каждого запроса
        gc.collect()
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
        
        return {'text': text, 'translation': translation}
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        # Очистка памяти даже при ошибке
        gc.collect()
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@app.get('/health')
async def health_check():
    """Проверка состояния сервиса и памяти"""
    try:
        # Проверяем использование памяти
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Если память превышает 85%, считаем это критическим состоянием
        if memory_percent > 85:
            logger.error(f"Critical memory usage: {memory_percent}%")
            raise HTTPException(
                status_code=503, 
                detail=f"Service unhealthy: High memory usage {memory_percent}%"
            )
        
        # Если память превышает 80%, предупреждаем и очищаем память
        if memory_percent > 80:
            logger.warning(f"High memory usage: {memory_percent}%, performing cleanup")
            gc.collect()
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
        
        return {
            'status': 'healthy',
            'model_loaded': translator is not None,
            'memory_usage_percent': memory_percent,
            'memory_available_gb': memory.available / 1024**3
        }
    except HTTPException:
        # Перебрасываем HTTPException для корректного статуса
        raise
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")
