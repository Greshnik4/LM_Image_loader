#!/usr/bin/env python3
import sys
import json
import base64
import os
from pathlib import Path

def load_image_tool(arguments):
    """
    Функция загрузки изображения.
    Ожидает аргумент 'file_path'.
    Возвращает base64 строку и MIME тип.
    """
    file_path = arguments.get("file_path")
    
    if not file_path:
        return {"error": "Не указан путь к файлу (file_path)."}

    path = Path(file_path)
    
    # Проверка существования файла
    if not path.exists():
        return {"error": f"Файл не найден: {file_path}"}
    
    # Проверка расширения
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    if path.suffix.lower() not in allowed_extensions:
        return {"error": f"Неподдерживаемый формат. Разрешены: {', '.join(allowed_extensions)}"}

    try:
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Определение MIME типа
        mime_type = "image/jpeg" if path.suffix.lower() in ['.jpg', '.jpeg'] else \
                    "image/png" if path.suffix.lower() == '.png' else \
                    "image/gif" if path.suffix.lower() == '.gif' else \
                    "image/webp" if path.suffix.lower() == '.webp' else \
                    "image/bmp"
        
        return {
            "success": True,
            "file_name": path.name,
            "mime_type": mime_type,
            "base64_data": encoded_string,
            "size_bytes": path.stat().st_size
        }
    except Exception as e:
        return {"error": f"Ошибка при чтении файла: {str(e)}"}

def main():
    # LM Studio передает аргументы через stdin в виде JSON
    try:
        input_data = sys.stdin.read()
        if not input_data:
            print(json.dumps({"error": "Нет входных данных"}))
            return

        request = json.loads(input_data)
        arguments = request.get("arguments", {})
        
        result = load_image_tool(arguments)
        
        # Вывод результата в stdout для LM Studio
        print(json.dumps(result))
        
    except json.JSONDecodeError:
        print(json.dumps({"error": "Некорректный JSON на входе"}))
    except Exception as e:
        print(json.dumps({"error": f"Критическая ошибка скрипта: {str(e)}"}))

if __name__ == "__main__":
    main()
