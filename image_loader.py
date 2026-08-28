import asyncio
import base64
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from PIL import Image
import io

# Инициализация сервера
mcp = FastMCP("Image Loader")

@mcp.tool()
def load_image(file_path: str) -> str:
    """
    Загружает изображение из указанного файла и возвращает его в формате base64.
    Поддерживает: jpg, jpeg, png, gif, webp, bmp.
    
    Args:
        file_path: Полный путь к файлу изображения.
    
    Returns:
        JSON строка с данными: mime_type и base64_content.
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    
    supported_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    if path.suffix.lower() not in supported_extensions:
        raise ValueError(f"Неподдерживаемый формат: {path.suffix}. Разрешены: {supported_extensions}")

    # Открытие и конвертация изображения
    with Image.open(path) as img:
        # Конвертируем в RGB если есть альфа-канал (для PNG), чтобы избежать проблем с JPEG
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        buffer = io.BytesIO()
        # Сохраняем в оригинальном формате или принудительно в PNG/JPG
        save_format = "PNG" if path.suffix.lower() == ".png" else "JPEG"
        img.save(buffer, format=save_format)
        image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        mime_type = "image/png" if save_format == "PNG" else "image/jpeg"

    return json.dumps({
        "mime_type": mime_type,
        "base64_content": image_data,
        "original_path": str(path)
    })

if __name__ == "__main__":
    # Запуск сервера
    mcp.run()
