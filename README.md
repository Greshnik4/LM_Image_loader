# Image Loader Tool for LM Studio

Инструмент для загрузки изображений из файлов (jpg, png) для анализа в LM Studio.

## Описание

Этот инструмент позволяет модели самостоятельно загружать изображения из локальных файлов и преобразовывать их в формат base64, который может быть использован для визуального анализа.

## Установка

Никаких дополнительных зависимостей не требуется. Используется только стандартная библиотека Python.

## Использование

### Командная строка

```bash
python image_loader.py <путь_к_изображению>
```

### Примеры

```bash
# Загрузка PNG изображения
python image_loader.py /path/to/image.png

# Загрузка JPG изображения
python image_loader.py /path/to/image.jpg
```

### Выходные данные

Инструмент возвращает JSON-объект со следующей структурой:

#### Успешная загрузка:
```json
{
  "success": true,
  "message": "Image loaded successfully",
  "image_data": "data:image/png;base64,...",
  "base64_raw": "...",
  "file_info": {
    "filename": "image.png",
    "path": "/absolute/path/to/image.png",
    "size_bytes": 12345,
    "mime_type": "image/png"
  }
}
```

#### Ошибка:
```json
{
  "success": false,
  "error": "Описание ошибки",
  "image_data": null
}
```

## Поддерживаемые форматы

- `.jpg` / `.jpeg` - JPEG изображения
- `.png` - PNG изображения
- `.gif` - GIF изображения
- `.webp` - WebP изображения
- `.bmp` - BMP изображения

## Ограничения

- Максимальный размер файла: 10MB
- Файл должен существовать и быть доступным для чтения

## Интеграция с LM Studio

Для использования этого инструмента в LM Studio:

1. **Как функция вызова (Function Calling)**: Настройте модель вызывать этот скрипт через функцию tool calling с параметром `file_path`.

2. **Пример промпта для модели**:
   ```
   Для анализа изображения используйте команду:
   python image_loader.py <путь_к_файлу>
   
   Затем используйте поле image_data из результата для отправки изображения 
   в vision-модель.
   ```

3. **Использование в коде**:
   ```python
   import subprocess
   import json
   
   result = subprocess.run(
       ['python', 'image_loader.py', '/path/to/image.png'],
       capture_output=True,
       text=True
   )
   data = json.loads(result.stdout)
   
   if data['success']:
       # Используйте data['image_data'] для отправки в модель
       print(f"Изображение загружено: {data['file_info']}")
   else:
       print(f"Ошибка: {data['error']}")
   ```

## API для импорта

Вы также можете импортировать функции напрямую в свой Python-код:

```python
from image_loader import load_image

result = load_image('/path/to/image.png')
if result['success']:
    print(f"Размер: {result['file_info']['size_bytes']} байт")
    # Используйте result['image_data'] для передачи в модель
else:
    print(f"Ошибка: {result['error']}")
```
