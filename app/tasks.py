import logging

logger = logging.getLogger("shop.tasks")

def log_upload_event(user_id: int, product_id: int, filename: str) -> None:
    # Имитация долгой операции (например, отправка уведомления)
    logger.info(f"Пользователь {user_id} загрузил файл {filename} для товара {product_id}")