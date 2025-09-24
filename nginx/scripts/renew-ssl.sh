#!/bin/bash

# Путь к папке проекта (укажите полный путь или используйте $(dirname "$0"))
PROJECT_DIR="/home/user1/bur_translator"

# Лог-файл
LOG_FILE="$PROJECT_DIR/nginx/logs/certbot-renew.log"

# Переходим в папку проекта
cd "$PROJECT_DIR" || { echo "❌ Не удалось перейти в $PROJECT_DIR" >> "$LOG_FILE"; exit 1; }

echo "[$(date)] 🔄 Запуск обновления сертификатов..." >> "$LOG_FILE"

# Обновляем сертификаты
certbot renew \
  --webroot \
  -w "$PROJECT_DIR/nginx/www/certbot" \
  --deploy-hook "docker compose exec nginx nginx -s reload" \
  >> "$LOG_FILE" 2>&1

# Проверяем код возврата
if [ $? -eq 0 ]; then
    echo "✅ Обновление успешно завершено" >> "$LOG_FILE"
else
    echo "❌ Ошибка при обновлении сертификатов" >> "$LOG_FILE"
fi

echo "--------------------------------------------------" >> "$LOG_FILE"