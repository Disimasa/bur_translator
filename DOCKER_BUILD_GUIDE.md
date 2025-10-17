# Руководство по сборке Docker

## Режимы сборки

### 1. Разработка (Development)
```bash
# Использует Dockerfile.dev
docker-compose -f docker-compose.dev.yml up --build
```
- **Dockerfile**: `Dockerfile.dev`
- **Режим**: development
- **Команда**: `pnpm run dev`
- **Особенности**: hot reload, sourcemap, быстрая сборка

### 2. Продакшен (Production)
```bash
# Использует основной Dockerfile
docker-compose up --build
```
- **Dockerfile**: `Dockerfile`
- **Режим**: production
- **Команда**: `pnpm run build:prod`
- **Особенности**: terser минификация, удаление console.log, оптимизация

## Переменные окружения

### Development
- `NODE_ENV=development`
- `VITE_MODE=development`

### Production
- `NODE_ENV=production`
- `VITE_MODE=production`

## Оптимизации продакшена

### 1. Сборка
- **Минификация**: terser (максимальная)
- **Sourcemap**: отключен
- **Console.log**: удалены
- **Размер чанков**: ограничен до 500KB

### 2. Docker
- **Multi-stage build**: оптимизация размера образа
- **Кэширование**: pnpm store
- **Память**: ограничена до 4GB для сборки

## Команды для сборки

```bash
# Только frontend в продакшене
docker build -f frontend/Dockerfile -t bur-translator-frontend ./frontend

# Полная сборка продакшена
docker-compose up --build

# Разработка
docker-compose -f docker-compose.dev.yml up --build
```

## Проверка режима

После сборки можно проверить, что приложение собрано в правильном режиме:
- В продакшене не должно быть `console.log` в коде
- Sourcemap файлы должны отсутствовать
- Размер бандла должен быть минимальным
