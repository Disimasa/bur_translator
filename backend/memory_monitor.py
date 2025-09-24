#!/usr/bin/env python3
"""
Скрипт для мониторинга использования памяти PyTorch на CPU
"""
import torch
import psutil
import time
import logging
import gc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_memory_usage():
    """Логирует текущее использование памяти"""
    # Системная память
    memory = psutil.virtual_memory()
    logger.info(f"System Memory: {memory.percent}% used ({memory.used / 1024**3:.2f}GB / {memory.total / 1024**3:.2f}GB)")
    
    # Процесс память
    process = psutil.Process()
    process_memory = process.memory_info()
    logger.info(f"Process Memory: {process_memory.rss / 1024**3:.2f}GB RSS, {process_memory.vms / 1024**3:.2f}GB VMS")
    
    # PyTorch память (если есть тензоры в памяти)
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            allocated = torch.cuda.memory_allocated(i) / 1024**3
            reserved = torch.cuda.memory_reserved(i) / 1024**3
            max_allocated = torch.cuda.max_memory_allocated(i) / 1024**3
            logger.info(f"CUDA {i}: Allocated={allocated:.2f}GB, Reserved={reserved:.2f}GB, Max={max_allocated:.2f}GB")

def cleanup_memory():
    """Принудительная очистка памяти"""
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
    logger.info("Memory cleanup completed")

def check_memory_leak():
    """Проверяет возможную утечку памяти"""
    memory = psutil.virtual_memory()
    if memory.percent > 90:
        logger.warning(f"High memory usage: {memory.percent}%")
        cleanup_memory()

if __name__ == "__main__":
    logger.info("Starting memory monitor for CPU-only PyTorch...")
    while True:
        log_memory_usage()
        check_memory_leak()
        time.sleep(60)  # Логируем каждую минуту
